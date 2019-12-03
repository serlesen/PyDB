import time
import uuid

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

    def push_search(self, collection, search_query, threads):
        search_id = str(uuid.uuid4())
        self.queries[search_id] = {'threads': threads, 'collection': collection, 'search_query': search_query}
        self.pending_results[search_id] = threads
        self.results[search_id] = []
        return search_id

    def push_results(self, results, search_id, thread_id):

        pending = self.pending_results[search_id]
        pending.remove(thread_id)
        if len(pending) == 0:
            del self.pending_results[search_id]

        self.results[search_id].extends(results)

    def pop_search(self, thread_id):
        for k, v in self.queries.items():
            if thread_id in v['threads']:
                v['threads'].remove(thread_id)
                return q
                
        # FIXME maybe throw an exception
        return None

    def pop_results(self, search_id):
        while search_id in self.pending_results:
            time.sleep(DatabaseContext.THREADS_CYCLE)
        return self.results.pop(search_id)

    def get_details(self):
        return self.queries

    def contains_data(self):
        return len(self.queries) > 0
