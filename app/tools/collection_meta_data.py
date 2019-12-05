import os

from app.exceptions.app_exception import AppException
from app.tools.database_context import DatabaseContext

#
# Class which contains all the meta information about a collection (count, name of the indexes, counter of the data files)
# line 1: counter of the last data file
# line 2: dict with the indexes -> key = field; value = amount of indexed elements
#
class CollectionMetaData(object):

    META_DATA_FILE_NAME = 'meta_data.txt'
    DATA_FILE_NAME = 'data{}.bin'
    INDEX_FILE_NAME = '{}.idx'

    def __init__(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection) is False:
            raise AppException('Collection {} doesn\'t exist'.format(collection), 404)

        self.collection = collection
        fname = DatabaseContext.DATA_FOLDER + self.collection + '/' + self.META_DATA_FILE_NAME 
        if os.path.exists(fname) is False:
            with open(fname, 'a') as file:
                file.write('1\n')
                file.write('{}\n')
        
        with open(fname, 'r') as file:
            file.seek(0)
            self.counter = int(file.readline())
            self.indexes = eval(file.readline())

    def add_or_update_index_count(self, field, count):
        self.indexes[field] = count
        self.update_meta_data(str(self.indexes), 2)
        return {'status': 'done'}
            
    def remove_index_count(self, field):
        if field not in self.indexes:
            return {'status': 'missing index'}
        del self.indexes[field]
        self.update_meta_data(str(self.indexes), 2)
        return {'status': 'done'}

    def enumerate_data_fnames(self, thread_id):
        fnames = []
        for i in range(self.counter):
            if thread_id == None or ((i + 1) % DatabaseContext.MAX_THREADS) == thread_id:
                fnames.append(self.DATA_FILE_NAME.format(i + 1))
        return fnames

    def enumerate_index_fnames(self):
        fnames = []
        for f in self.indexes.keys():
            fnames.append(self.get_index_fname(f))
        return fnames

    def get_index_fname(self, field):
        return self.INDEX_FILE_NAME.format(field)

    def last_data_fname(self):
        return self.DATA_FILE_NAME.format(self.counter)

    def next_data_fname(self):
        self.counter = int(self.update_meta_data(str(self.counter + 1), 1))
        return self.DATA_FILE_NAME.format(self.counter)

    def remove_last_data_file(self):
        if self.counter > 1:
            self.counter = int(self.update_meta_data(str(self.counter - 1), 1))
            os.remove(DatabaseContext.DATA_FOLDER + self.collection + '/' + self.DATA_FILE_NAME.format(self.counter + 1))
        else:
            os.remove(DatabaseContext.DATA_FOLDER + self.collection + '/' + self.DATA_FILE_NAME.format(self.counter))
        return self.DATA_FILE_NAME.format(self.counter)

    def update_meta_data(self, value, line_nb):
        fname = DatabaseContext.DATA_FOLDER + self.collection + '/' + self.META_DATA_FILE_NAME 
        with open(fname, 'r') as file:
            all_lines = file.readlines()
        with open(fname, 'w') as file:
            for i, line in enumerate(all_lines, 1):
                if i == line_nb:
                    file.writelines(value + '\n')
                else:
                    file.writelines(line)
        return value

