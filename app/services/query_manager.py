from app.exceptions.app_exception import AppException
from app.threads.query_stack import QueryStack
from app.threads.replication_stack import ReplicationStack

class QueryManager(object):

    def search(self, collection, search_query):
        query_id = QueryStack.get_instance().push_search(collection, search_query)
        return QueryStack.get_instance().pop_results(query_id)

    def get_one(self, collection, doc_id):
        query_id = QueryStack.get_instance().push_search(collection, {"$filter":{"id": doc_id}})
        results = QueryStack.get_instance().pop_results(query_id)
        if len(results) != 1:
            return None
        return results[0]

    def upsert(self, collection, doc):
        query_id = QueryStack.get_instance().push_upsert(collection, doc)
        ReplicationStack.get_instance().push_upsert(collection, doc)
        return QueryStack.get_instance().pop_results(query_id)

    def patch(self, collection, previous_doc, doc):
        query_id = QueryStack.get_instance().push_patch(collection, previous_doc, doc)
        ReplicationStack.get_instance().push_patch(collection, previous_doc, doc)
        return QueryStack.get_instance().pop_results(query_id)

    def delete(self, collection, doc_id):
        query_id = QueryStack.get_instance().push_delete(collection, doc_id)
        ReplicationStack.get_instance().push_delete(collection, doc_id)
        return QueryStack.get_instance().pop_results(query_id)
