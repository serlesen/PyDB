#
# Class which contains constants for the database behavior.
#
class DatabaseContext(object):
    CACHE_FILE_SIZE = 100 # in Mb
    DATA_FOLDER = 'data/'
    DEFAULT_RESULTS_SIZE = 10
    DEFAULT_RESULTS_SKIP = 0
    LOCKING_CYCLE = 0.01
    THREADS_CYCLE = 0.1
    THREADS_MANAGER_CYCLING = True
    MAX_DOC_PER_FILE = 100000
    MAX_THREADS = 24