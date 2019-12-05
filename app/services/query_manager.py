from app.threads.query_stack import QueryStack

class QueryManager(object):

    def search(self, collection, search_query):
        query_id = QueryStack.get_instance().push_search(collection, search_query)
        return QueryStack.get_instance().pop_results(query_id)

    def get_one(self, collection, doc_id):
        query_id = QueryStack.get_instance().push_search(collection, {"$filter":{"id": doc_id}})
        return QueryStack.get_instance().pop_results(query_id)

    def create(self, collection, doc):
        query_id = QueryStack.get_instance().push_create(collection, doc)
        return QueryStack.get_instance().pop_results(query_id)

    def update(self, collection, doc, doc_id):
        query_id = QueryStack.get_instance().push_update(collection, doc, doc_id)
        return QueryStack.get_instance().pop_results(query_id)

    def delete(self, collection, doc_id):
        query_id = QueryStack.get_instance().push_delete(collection, doc_id)
        return QueryStack.get_instance().pop_results(query_id)