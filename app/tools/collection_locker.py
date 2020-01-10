import os
import re
import time

from app.tools.database_context import DatabaseContext

def col_locking(func):
    def wrapper(*args, **kwargs):
        # first arg is self, second arg is col_meta_data
        col_meta_data = args[1]

        CollectionLocker.wait_for_lock(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER)

        return func(*args, **kwargs)
    return wrapper

def file_locking(func):
    def wrapper(*args, **kwargs):
        # first arg is self, second arg is pname
        pname = args[1]

        m = re.match(r'(.*)/([-_a-zA-Z]*)/([-_a-zA-Z0-9]*)\.(bin|idx)', pname)
        CollectionLocker.wait_for_lock(m.group(1) + '/' + m.group(2) + '/' + CollectionLocker.LOCK_FOLDER)
        CollectionLocker.wait_for_lock(pname)

        with open(CollectionLocker.LOCK_FILE.format(pname), 'w') as file:
            file.write('x')

        result = func(*args, **kwargs)

        os.remove(CollectionLocker.LOCK_FILE.format(pname))
    return wrapper

class CollectionLocker(object):
    """ Class to handle the lock on collections and single files.
    Only the decorator is outside the class (to ease the way to call it)
    """
    
    LOCK_FILE = '{}.lock'
    LOCK_FOLDER = 'col.lock'

    @staticmethod
    def lock_col(col_meta_data):
        # check collection is not locked
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER
        CollectionLocker.wait_for_lock(pname)

        # check data files are not locked
        for f in col_meta_data.enumerate_data_fnames(None):
            CollectionLocker.wait_for_lock(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + f)
            
        # check indexes files are not locked
        for f in col_meta_data.enumerate_index_fnames():
            CollectionLocker.wait_for_lock(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + f)
        
        with open(pname, 'w') as file:
            file.write('x')

    @staticmethod
    def unlock_col(col_meta_data):
        os.remove(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER)

    def wait_for_lock(pname):
        while os.path.exists(CollectionLocker.LOCK_FILE.format(pname)):
            time.sleep(DatabaseContext.LOCKING_CYCLE)

