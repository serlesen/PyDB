from itertools import count
from threading import Thread
import _pickle as pickle

from app.services.files_reader import FilesReader
from app.threads.cleaning_stack import CleaningStack
from app.tools.collection_locker import CollectionLocker
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CleaningThread(Thread):
    """ Class to handle the cleaning of the deleted documents.
    When deleting a document, it's replaced by an empty document and the index still unchanged.
    This class (run in a separated thread) will check those empty documents, remove them and
    update the indexes consequently.
    """

    def __init__(self):
        Thread.__init__(self)
        self.item = CleaningStack.get_instance().pop()
        self.col_meta_data = CollectionMetaData(self.item['collection'])
        self.incoming_line = self.item['line']

    def run(self):
        try:
            CollectionLocker.lock_col(self.col_meta_data)
    
            self.swift_data_docs()
     
            self.update_indexes_file()

            self.update_remaining_cleanings()

            CollectionLocker.unlock_col(self.col_meta_data)
        except Exception as e:
            print(f'Cleaning thread failed with {e}')

    def swift_data_docs(self):
        """ Method to move documents from a data file to a previous data file.
        The data files must have a constant file length (except the last). When
        removing a document from the middle of a data file, we must add another
        document at the end, this document must come from the beginning of the
        next data file.
        """
        doc_to_move = None
        fnames = self.col_meta_data.enumerate_data_fnames(None) 
        for i, fname in zip(count(len(fnames) - 1, -1), reversed(fnames)):
            if self.incoming_line >= (i + 1) * DatabaseContext.MAX_DOC_PER_FILE:
                # the incoming line is in a higher data file
                continue
            if self.incoming_line < i * DatabaseContext.MAX_DOC_PER_FILE:
                # the incoming line is in a lower data file
                line_to_pop = 0
            elif self.incoming_line < (i + 1) * DatabaseContext.MAX_DOC_PER_FILE and self.incoming_line >= i * DatabaseContext.MAX_DOC_PER_FILE:
                # the incoming line is in the present data file
                line_to_pop = self.incoming_line % DatabaseContext.MAX_DOC_PER_FILE

            pname = DatabaseContext.DATA_FOLDER + self.col_meta_data.collection + '/' + fname

            with open(pname, 'rb+') as file:
                docs = pickle.load(file)
                file.seek(0)
                file.truncate()
                if doc_to_move is not None:
                    docs.append(doc_to_move)
                doc_to_move = docs.pop(line_to_pop)
                file.write(pickle.dumps(docs))

            if len(docs) == 0:
                self.col_meta_data.remove_last_data_file()

            FilesReader.get_instance().invalidate_file_content(pname)

    def update_indexes_file(self):
        """ Method to update the new line of each doc in the indexes file.
        After swifting the documents because of a deleting, each document will
        be placed in a lower line.
        """
        for field in self.col_meta_data.indexes.keys():
            pname = DatabaseContext.DATA_FOLDER + self.col_meta_data.collection + '/' + self.col_meta_data.get_index_fname(field)
 
            with open(pname, 'rb+') as file:
                values = pickle.load(file)
                file.seek(0)
                file.truncate()

                updated_values = {}
                for k, lines in values.items():
                    updated_lines = []
                    for l in lines:
                        if l > self.incoming_line:
                            updated_lines.append(l - 1)
                        elif l != self.incoming_line:
                            updated_lines.append(l)
                    if len(updated_lines) > 0:
                        updated_values[k] = updated_lines

                file.write(pickle.dumps(updated_values))
            FilesReader.get_instance().invalidate_file_content(pname)

            self.col_meta_data.add_or_update_index_count(field, self.col_meta_data.indexes[field] - 1)

    def update_remaining_cleanings(self):
        """ Method to update the line reference of the incoming cleaning requests.
        The case: two or more documents were deleted at same time; the first removed
        document was completly removed, the rest of the documents swifted and the lines
        updated; the other removed documents had their lines updated in the index files
        but we also have to update the cleaning stack as it's pointing to an old location.
        """
        for i in CleaningStack.get_instance().stack:
            if i['collection'] == self.col_meta_data.collection and i['line'] > self.incoming_line:
                i['line'] -= 1
