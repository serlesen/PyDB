import time
from threading import Thread

from app.threads.cleaning_stack import CleaningStack
from app.threads.cleaning_thread import CleaningThread
from app.threads.query_stack import QueryStack
from app.threads.query_thread import QueryThread
from app.threads.replication_stack import ReplicationStack
from app.threads.replication_thread import ReplicationThread
from app.tools.database_context import DatabaseContext

class ThreadsManager(Thread):
    """ Class that create new threads to handle different actions asychronously. """

    def run(self):
        available_threads = DatabaseContext.MAX_THREADS

        while DatabaseContext.THREADS_MANAGER_CYCLING:

            try:
                if len(DatabaseContext.SLAVES) > 0 and ReplicationStack.get_instance().contains_data():
                    ReplicationThread().start()
    
                if CleaningStack.get_instance().contains_data():
                    CleaningThread().start()
    
                threads_by_query = QueryStack.get_instance().threads_needed()
                if threads_by_query is not None:
                    for t in threads_by_query['threads']:
                        QueryThread(threads_by_query['query_id'], t).start()
    
                time.sleep(DatabaseContext.THREADS_CYCLE)
            except Exception as e:
                print(f'Threads manager failed with {e}')
