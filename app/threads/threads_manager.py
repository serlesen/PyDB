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

        while True:

            if CleaningStack.get_instance().contains_data():
                CleaningThread().start()

            if SearchingStack.get_instance().contains_data():
                for i in range(available_threads):
                    SearchingThread(i).start()

            time.sleep(DatabaseContext.THREADS_CYCLE)
