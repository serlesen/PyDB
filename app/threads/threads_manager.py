import time
from threading import Thread

from app.threads.cleaning_stack import CleaningStack
from app.threads.cleaning_thread import CleaningThread
from app.threads.searching_stack import SearchingStack
from app.threads.searching_thread import SearchingThread
from app.tools.database_context import DatabaseContext

class ThreadsManager(Thread):

    def run(self):
        available_threads = DatabaseContext.MAX_THREADS

        while DatabaseContext.THREADS_MANAGER_CYCLING:

            if CleaningStack.get_instance().contains_data():
                CleaningThread().start()

            threads_by_search = SearchingStack.get_instance().threads_needed()
            if threads_by_search is not None:
                for t in threads_by_search['threads']:
                    SearchingThread(threads_by_search['search_id'], t).start()

            time.sleep(DatabaseContext.THREADS_CYCLE)
