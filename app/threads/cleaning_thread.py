from threading import Thread
import _pickle as pickle

from app.services.indexes_service import IndexesService
from app.threads.cleaning_stack import CleaningStack
from app.tools.collection_locker import CollectionLocker
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CleaningThread(Thread):

    def __init__(self):
        self.indexes_service = IndexesService()

    def run(self):
        item = CleaningStack.get_instance().pop()

        col_meta_data = CollectionMetaData(item['collection'])
        line = item['line']

        pname = self.find_data_file(col_meta_data, line)

        CollectionLocker.lock_col(col_meta_data)
 
        # Remove the document from the data files
        with open(pname, 'rb+') as file:
            docs = pickle.load(file)
            file.seek(0)
            file.truncate()
            docs.pop(line)
            file.write(pickle.dumps(docs))
 
        # Update the indexes line
#        for f in self.indexes_service.enumerate_index_fnames(col_meta_data):
#            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + f
# 
#            with open(pname, 'rb+') as file:
#                values = pickle.load(file)
#                file.seek(0)
#                file.truncate()
#                for v in values.keys():
#                    if v > line:
#                        d = values[v]
#                        values.remove(v)
#                        new_line = v - 1
#                        values[new_line] = d
#                    elif v == line:
#                        values.remove(v)
#                file.write(pickle.dumps(values))
 
        CollectionLocker.unlock_col(col_meta_data)

    def find_data_file(self, col_meta_data, line):
        for i, fname in enumerate(col_meta_data.enumerate_data_fnames()):
            if line > (i + 1) * DatabaseContext.MAX_DOC_PER_FILE:
                continue
            return DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + fname
