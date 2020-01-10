from app.tools.database_context import DatabaseContext

class ReplicationStack(object):
    """ Class which holds all the queries which imply a modification and needs to
    be replicated to the slaves (if configured).
    """

    instance = None

    def __init__(self):
        self.queries = []
        self.errors = []

    def get_instance():
        if ReplicationStack.instance is None:
            ReplicationStack.instance = ReplicationStack()
        return ReplicationStack.instance

    def push_upsert(self, collection, doc):
        for slave in DatabaseContext.SLAVES.keys():
            self.queries.append({'collection': collection, 'url': slave, 'doc': doc})

    def push_patch(self, collection, previous_doc, doc):
        for slave in DatabaseContext.SLAVES.keys():
            self.queries.append({'collection': collection, 'url': slave, 'previous_doc': previous_doc, 'doc': doc})

    def push_delete(self, collection, search_query):
        for slave in DatabaseContext.SLAVES.keys():
            self.queries.append({'collection': collection, 'url': slave, 'search_query': search_query})

    def push_error(self, item):
        self.errors.append(item)

    def pop(self):
        return self.queries.pop(0)

    def get_details(self):
        return self.queries

    def contains_data(self):
        return len(self.queries) > 0
