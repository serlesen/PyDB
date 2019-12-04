import time
import uuid

from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class SearchingStack(object):

    instance = None

    def __init__(self):
        self.queries = {}
        self.pending_results = {}
        self.results = {}

    def get_instance():
        if SearchingStack.instance is None:
            SearchingStack.instance = SearchingStack()
        return SearchingStack.instance

    def push_search(self, collection, search_query):
        search_id = str(uuid.uuid4())
        self.pending_results[search_id] = list(range(1, CollectionMetaData(collection).counter + 1))
        self.results[search_id] = []
        self.queries[search_id] = {'collection': collection, 'search_query': search_query, 'started': False}
        return search_id

    def push_results(self, results, search_id, thread_id):
        pending = self.pending_results[search_id]
        pending.remove(thread_id)
        if len(pending) == 0:
            del self.pending_results[search_id]

        self.results[search_id].extend(results)

    def pop_search(self, search_id):
        return self.queries[search_id]

    def pop_results(self, search_id):
        while search_id in self.pending_results:
            time.sleep(DatabaseContext.THREADS_CYCLE)
        return self.results.pop(search_id)

    def get_details(self):
        return self.queries

    def threads_needed(self):
        for k, v in self.queries.items():
            if v['started'] is False:
                v['started'] = True
                return {'search_id': k, 'threads': self.pending_results[k]}
        return None
