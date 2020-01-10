import time
import uuid

from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class QueryStack(object):
    """ Class to hold all the search that must be made.
    This class is necessarry to allow the searches being done in multiple threads
    which will decrease the response time when searching for a document.
    """

    instance = None

    def __init__(self):
        self.queries = {}
        self.pending_results = {}
        self.results = {}
        self.errors = {}

    def get_instance():
        if QueryStack.instance is None:
            QueryStack.instance = QueryStack()
        return QueryStack.instance

    def push_search(self, collection, search_query):
        return self.push_action(collection, search_query, None, None, 'search')

    def push_upsert(self, collection, doc):
        return self.push_action(collection, None, None, doc, 'upsert')

    def push_patch(self, collection, previous_doc, doc):
        return self.push_action(collection, None, previous_doc, doc, 'patch')

    def push_delete(self, collection, search_query):
        return self.push_action(collection, search_query, None, None, 'delete')

    def push_action(self, collection, search_query, previous_doc, doc, action):
        query_id = str(uuid.uuid4())
        self.pending_results[query_id] = self.build_threads_need(collection, action)
        self.results[query_id] = []
        self.queries[query_id] = {'collection': collection, 'action': action, 'search_query': search_query, 'previous_doc': previous_doc, 'doc': doc, 'started': False}
        return query_id

    def build_threads_need(self, collection, action):
        if action == 'search':
            return list(range(1, CollectionMetaData(collection).counter + 1))
        if action == 'upsert':
            return [1]
        if action == 'patch':
            return [1]
        if action == 'delete':
            return [1]

    def push_error(self, error, query_id):
        self.errors[query_id] = error

        del self.pending_results[query_id]

    def push_results(self, results, query_id, thread_id):
        if isinstance(results, list):
            self.results[query_id].extend(results)
        else:
            self.results[query_id] = results

        pending = self.pending_results[query_id]
        pending.remove(thread_id)
        if len(pending) == 0:
            del self.pending_results[query_id]

    def pop_action(self, query_id):
        return self.queries[query_id]

    def pop_results(self, query_id):
        while query_id in self.pending_results:
            time.sleep(DatabaseContext.THREADS_CYCLE)

        del self.queries[query_id]

        if query_id in self.errors:
            raise self.errors.pop(query_id)
        return self.results.pop(query_id)

    def get_details(self):
        return self.queries

    def threads_needed(self):
        for k, v in self.queries.items():
            if v['started'] is False:
                v['started'] = True
                return {'query_id': k, 'threads': self.pending_results[k]}
        return None
