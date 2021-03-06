from threading import Thread

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.search_service import SearchService
from app.services.crud_service import CrudService
from app.threads.query_stack import QueryStack
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.search_context import SearchContext

class QueryThread(Thread):
    """ Thread that run the search queries stored in QueryStack. """

    def __init__(self, query_id, thread_id):
        Thread.__init__(self)
        self.search_service = DependencyInjectionsService.get_instance().get_service(SearchService)
        self.crud_service = DependencyInjectionsService.get_instance().get_service(CrudService)
        self.query_id = query_id
        self.thread_id = thread_id
        self.item = QueryStack.get_instance().pop_action(self.query_id)

    def run(self):
        try:
            if self.item == None:
                return

            if self.item['action'] == 'search':
                results = self.search_service.search_by_thread(CollectionMetaData(self.item['collection']), SearchContext(self.item['search_query']), self.thread_id)
            elif self.item['action'] == 'upsert':
                results = self.crud_service.upsert(CollectionMetaData(self.item['collection']), self.item['docs'])
            elif self.item['action'] == 'patch':
                results = self.crud_service.patch(CollectionMetaData(self.item['collection']), self.item['previous_doc'], self.item['doc'])
            elif self.item['action'] == 'delete':
                results = self.crud_service.delete(CollectionMetaData(self.item['collection']), self.item['search_query'])

            QueryStack.get_instance().push_results(results, self.query_id, self.thread_id)
        except Exception as e:
            print(f'Query thread failed with {e}')
            QueryStack.get_instance().push_error(e, self.query_id)

