from itertools import count
from threading import Thread
import _pickle as pickle

from app.services.files_reader import FilesReader
from app.threads.cleaning_stack import CleaningStack
from app.tools.collection_locker import CollectionLocker
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CleaningThread(Thread):

    def run(self):
        item = CleaningStack.get_instance().pop()

        col_meta_data = CollectionMetaData(item['collection'])
        incoming_line = item['line']

        CollectionLocker.lock_col(col_meta_data)

        self.swift_data_docs(col_meta_data, incoming_line)
 
        self.update_indexes_file(col_meta_data, incoming_line)

        CollectionLocker.unlock_col(col_meta_data)

    def swift_data_docs(self, col_meta_data, incoming_line):
        doc_to_move = None
        fnames = col_meta_data.enumerate_data_fnames(None) 
        for i, fname in zip(count(len(fnames) - 1, -1), reversed(fnames)):
            if incoming_line > (i + 1) * DatabaseContext.MAX_DOC_PER_FILE:
                continue
            if incoming_line < i * DatabaseContext.MAX_DOC_PER_FILE:
                line_to_pop = 0
            elif incoming_line < (i + 1) * DatabaseContext.MAX_DOC_PER_FILE and incoming_line > i * DatabaseContext.MAX_DOC_PER_FILE:
                line_to_pop = incoming_line
            
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname

            with open(pname, 'rb+') as file:
                docs = pickle.load(file)
                file.seek(0)
                file.truncate()
                if doc_to_move is not None:
                    docs.append(doc_to_move)
                doc_to_move = docs.pop(line_to_pop)
                file.write(pickle.dumps(docs))
            FilesReader.get_instance().invalidate_file_content(pname)

    def update_indexes_file(self, col_meta_data, incoming_line):
        for field in col_meta_data.indexes.keys():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.get_index_fname(field)
 
            with open(pname, 'rb+') as file:
                values = pickle.load(file)
                file.seek(0)
                file.truncate()

                updated_values = {}
                for k, lines in values.items():
                    updated_lines = []
                    for l in lines:
                        if l > incoming_line:
                            updated_lines.append(l - 1)
                        elif l != incoming_line:
                            updated_lines.append(l)
                    if len(updated_lines) > 0:
                        updated_values[k] = updated_lines

                file.write(pickle.dumps(updated_values))
            FilesReader.get_instance().invalidate_file_content(pname)

            col_meta_data.add_or_update_index_count(field, col_meta_data.indexes[field] - 1)
