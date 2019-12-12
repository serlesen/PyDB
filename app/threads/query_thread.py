from threading import Thread

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.search_service import SearchService
from app.services.crud_service import CrudService
from app.threads.query_stack import QueryStack
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.search_context import SearchContext

class QueryThread(Thread):

    def __init__(self, query_id, thread_id):
        Thread.__init__(self)
        self.search_service = DependencyInjectionsService.get_instance().get_service(SearchService)
        self.crud_service = DependencyInjectionsService.get_instance().get_service(CrudService)
        self.query_id = query_id
        self.thread_id = thread_id

    def run(self):
        item = QueryStack.get_instance().pop_action(self.query_id)
        if item == None:
            return

        try:
            if item['action'] == 'search':
                results = self.search_service.search_by_thread(CollectionMetaData(item['collection']), SearchContext(item['search_query']), self.thread_id)
            elif item['action'] == 'create':
                results = self.crud_service.create(CollectionMetaData(item['collection']), item['doc'])
            elif item['action'] == 'update':
                results = self.crud_service.update(CollectionMetaData(item['collection']), item['doc_id'], item['doc'])
            elif item['action'] == 'delete':
                results = self.crud_service.delete(CollectionMetaData(item['collection']), item['doc_id'])

            QueryStack.get_instance().push_results(results, self.query_id, self.thread_id)
        except Exception as e:
            QueryStack.get_instance().push_error(e, self.query_id)

