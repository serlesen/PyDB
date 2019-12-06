import _pickle as pickle

from sys import getsizeof

from app.tools.collection_locker import CollectionLocker
from app.tools.database_context import DatabaseContext

class FilesReader(object):

    instance = None

    def __init__(self):
        self.files = {}
        self.available_space = DatabaseContext.CACHE_FILE_SIZE

    def get_instance():
        if FilesReader.instance is None:
            FilesReader.instance = FilesReader()
        return FilesReader.instance

    def reset(self):
        FilesReader.instance = FilesReader()

    def get_file_content(self, pname):
        if pname in self.files:
            return self.files[pname]

        with open(pname, 'rb') as file:
            values = pickle.load(file)

        self.files[pname] = values

        self.available_space -= getsizeof(values)

        if self.available_space < 0:
            self.remove_oldest_file_content()

        return self.files[pname]

    # use decorator for locking file instead
    def write_file_content(self, pname, docs):
        CollectionLocker.lock_file(pname)
        with open(pname, "wb") as file:
            file.write(pickle.dumps(docs))

        self.invalidate_file_content(pname)

        CollectionLocker.unlock_file(pname)

    def invalidate_file_content(self, pname):
        if pname in self.files:
            del self.files[pname]

    def remove_oldest_file_content(self):
        pass