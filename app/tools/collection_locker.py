import os
import time

from app.tools.database_context import DatabaseContext

def col_locking(func):
    def wrapper(*args, **kwargs):
        # first arg is self, second arg is col_meta_data
        col_meta_data = args[1]

        CollectionLocker.wait_for_lock(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER)

        return func(*args, **kwargs)
    return wrapper

class CollectionLocker(object):
    
    LOCK_FILE = '{}.lock'
    LOCK_FOLDER = 'col.lock'
    
    @staticmethod
    def lock_file(pname):
        CollectionLocker.wait_for_lock(pname)

        with open(CollectionLocker.LOCK_FILE.format(pname), 'w') as file:
            file.write('x')

    @staticmethod
    def unlock_file(pname):
        os.remove(CollectionLocker.LOCK_FILE.format(pname))

    @staticmethod
    def lock_col(col_meta_data):

        # check data files are not locked
        for f in col_meta_data.enumerate_data_fnames():
            CollectionLocker.wait_for_lock(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + f)
            
        # to avoid circular dependency, import right before use it
        from app.services.indexes_service import IndexesService

        # check indexes files are not locked
        for f in IndexesService.enumerate_index_fnames(col_meta_data):
            CollectionLocker.wait_for_lock(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + f)
        
        # check collection is not locked
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER
        CollectionLocker.wait_for_lock(pname)

        with open(pname, 'w') as file:
            file.write('x')

    @staticmethod
    def unlock_col(col_meta_data):
        os.remove(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER)

    def wait_for_lock(pname):
        while os.path.exists(CollectionLocker.LOCK_FILE.format(pname)):
            time.sleep(DatabaseContext.LOCKING_CYCLE)

