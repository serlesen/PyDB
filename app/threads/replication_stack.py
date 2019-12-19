from app.tools.database_context import DatabaseContext

class ReplicationStack(object):

    instance = None

    def __init__(self):
        self.queries = []
        self.errors = []

    def get_instance():
        if ReplicationStack.instance is None:
            ReplicationStack.instance = ReplicationStack()
        return ReplicationStack.instance

    def push_upsert(self, collection, doc):
        for slave in DatabaseContext.SLAVES:
            self.queries.append({'collection': collection, 'url': slave, 'doc': doc})

    def push_delete(self, collection, id):
        for slave in DatabaseContext.SLAVES:
            self.queries.append({'collection': collection, 'url': slave, 'id': id})

    def push_error(self, item):
        self.errors.append(item)

    def pop(self):
        return self.queries.pop(0)

    def get_details(self):
        return self.queries

    def contains_data(self):
        return len(self.queries) > 0
