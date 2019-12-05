import time
from threading import Thread

from app.threads.cleaning_stack import CleaningStack
from app.threads.cleaning_thread import CleaningThread
from app.threads.query_stack import QueryStack
from app.threads.query_thread import QueryThread
from app.tools.database_context import DatabaseContext

class ThreadsManager(Thread):

    def run(self):
        available_threads = DatabaseContext.MAX_THREADS

        while DatabaseContext.THREADS_MANAGER_CYCLING:

            if CleaningStack.get_instance().contains_data():
                CleaningThread().start()

            threads_by_query = QueryStack.get_instance().threads_needed()
            if threads_by_query is not None:
                for t in threads_by_query['threads']:
                    QueryThread(threads_by_query['query_id'], t).start()

            time.sleep(DatabaseContext.THREADS_CYCLE)
