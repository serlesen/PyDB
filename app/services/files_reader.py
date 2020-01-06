import _pickle as pickle

from datetime import datetime
from sys import getsizeof

from app.tools.collection_locker import file_locking, CollectionLocker
from app.tools.database_context import DatabaseContext


class FilesReader(object):
    """ Class to read and write the content of a file.
    This class also handles a cache for frequently used files.
    This class also handles the locking.
    """

    instance = None

    def __init__(self):
        self.files = {}
        self.available_space = DatabaseContext.CACHE_FILE_SIZE * 1048576

    def get_instance():
        if FilesReader.instance is None:
            FilesReader.instance = FilesReader()
        return FilesReader.instance

    def reset(self):
        FilesReader.instance = FilesReader()

    def get_file_content(self, pname):
        if pname in self.files:
            self.files[pname]['last_used'] = datetime.utcnow()
            return self.files[pname]['values']

        with open(pname, 'rb') as file:
            values = pickle.load(file)

        size = getsizeof(values)
        self.files[pname] = {'values': values, 'last_used': datetime.utcnow(), 'size': size}

        self.available_space -= size

        if self.available_space < 0:
            self.remove_oldest_file_content()

        return values

    @file_locking
    def write_file_content(self, pname, docs):
        with open(pname, "wb") as file:
            file.write(pickle.dumps(docs))

        self.invalidate_file_content(pname)

    def invalidate_file_content(self, pname):
        if pname in self.files:
            del self.files[pname]

    def remove_oldest_file_content(self):
        oldest_key = None
        for k in self.files.keys():
            if oldest_key is None:
                oldest_key = k
            elif self.files[oldest_key]['last_used'] > self.files[k]['last_used']:
                oldest_key = k

        self.available_space += self.files[oldest_key]['size']
        del self.files[oldest_key]
