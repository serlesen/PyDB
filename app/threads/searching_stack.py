import time
import uuid

from app.tools.database_context import DatabaseContext

class SearchingStack(object):

    instance = None

    def __init__(self):
        self.queries = []
        self.results = {}

    def get_instance():
        if SearchingStack.instance is None:
            SearchingStack.instance = SearchingStack()
        return SearchingStack.instance

    def push_search(self, collection, search_query):
        search_id = str(uuid.uuid4())
        self.queries.append({'id': search_id, 'collection': collection, 'search_query': search_query})
        return search_id

    def push_results(self, results, search_id):
        self.results[search_id] = results

    def pop_search(self):
        return self.queries.pop(0)

    def pop_results(self, search_id):
        while search_id not in self.results:
            time.sleep(DatabaseContext.THREADS_CYCLE)
        return self.results.pop(search_id)

    def get_details(self):
        return self.queries

    def contains_data(self):
        return len(self.queries) > 0
