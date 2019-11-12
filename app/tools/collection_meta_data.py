import os

from app.tools.database_context import DatabaseContext

#
# line 1: counter of the last data file
#
class CollectionMetaData(object):

    META_DATA_FILE_NAME = 'meta_data.txt'
    DATA_FILE_NAME = 'data{}.txt'

    def __init__(self, collection):
        self.collection = collection
        fname = DatabaseContext.DATA_FOLDER + self.collection + '/' + self.META_DATA_FILE_NAME 
        if os.path.exists(fname) is False:
            with open(fname, 'a') as file:
                file.write('1')
        
        with open(fname, 'r') as file:
            file.seek(0)
            self.counter = int(file.readline())
            
    def enumerate_data_fnames(self):
        fnames = []
        for i in range(self.counter):
            fnames.append(self.DATA_FILE_NAME.format(i + 1))
        return fnames

    def last_data_fname(self):
        return self.DATA_FILE_NAME.format(self.counter)

    def next_data_fname(self):
        self.counter = self.update_counter(self.counter + 1)
        return self.DATA_FILE_NAME.format(self.counter)

    def remove_last_data_file(self):
        if self.counter > 1:
            self.counter = self.update_counter(self.counter - 1)
            os.remove(DatabaseContext.DATA_FOLDER + self.collection + '/' + self.DATA_FILE_NAME.format(self.counter + 1))
        else:
            os.remove(DatabaseContext.DATA_FOLDER + self.collection + '/' + self.DATA_FILE_NAME.format(self.counter))
        return self.DATA_FILE_NAME.format(self.counter)

    def update_counter(self, value):
        fname = DatabaseContext.DATA_FOLDER + self.collection + '/' + self.META_DATA_FILE_NAME 
        with open(fname, 'r') as file:
            all_lines = file.readlines()
        with open(fname, 'w') as file:
            for i, line in enumerate(all_lines, 1):
                if i == 1:
                    file.writelines(str(value) + '\n')
                else:
                    file.writelines(line)
        return value

