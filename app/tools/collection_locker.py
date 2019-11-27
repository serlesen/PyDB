import os

class CollectionLocker(object):
    
    LOCK_FILE = '{}.lock'
    LOCK_FOLDER = 'col.lock'
    
    @staticmethod
    def lock_file(pname):
        while os.path.exists(CollectionLocker.LOCK_FILE.format(pname)):
            time.sleep(DatabaseContext.LOCKING_CYCLE)

        with open(CollectionLocker.LOCK_FILE.format(pname), 'w') as file:
            file.write('x')

    @staticmethod
    def unlock_file(pname):
        os.remove(CollectionLocker.LOCK_FILE.format(pname))

    @staticmethod
    def lock_col(col_meta_data):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER

        while os.path.exists(pname):
            time.sleep(DatabaseContext.LOCKING_CYCLE)

        with open(pname, 'w') as file:
            file.write('x')

    @staticmethod
    def check_col_locking(col_meta_data):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER

        while os.path.exists(pname):
            time.sleep(DatabaseContext.LOCKING_CYCLE)

    @staticmethod
    def unlock_col(col_meta_data):
        os.remove(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + CollectionLocker.LOCK_FOLDER)
