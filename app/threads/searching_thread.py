import datetime
from threading import Thread

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.search_service import SearchService
from app.threads.searching_stack import SearchingStack
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.search_context import SearchContext

class SearchingThread(Thread):

    def __init__(self, search_id, thread_id):
        Thread.__init__(self)
        self.search_service = DependencyInjectionsService.get_instance().get_service(SearchService)
        self.search_id = search_id
        self.thread_id = thread_id

    def run(self):
       item = SearchingStack.get_instance().pop_search(self.search_id)
       if item == None:
           return

       results = self.search_service.search(CollectionMetaData(item['collection']), SearchContext(item['search_query']), self.thread_id)

       SearchingStack.get_instance().push_results(results, self.search_id, self.thread_id)
