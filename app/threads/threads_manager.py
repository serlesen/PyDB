import time
from threading import Thread

from app.threads.cleaning_stack import CleaningStack
from app.threads.cleaning_thread import CleaningThread
from app.tools.database_context import DatabaseContext

class ThreadsManager(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.cleaning_thread = CleaningThread()

    def run(self):
        while True:

            if CleaningStack.get_instance().contains_data():
                self.cleaning_thread.start()

            time.sleep(DatabaseContext.THREADS_CYCLE)
