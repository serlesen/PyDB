class CleaningStack(object):

    instance = None

    def __init__(self):
        self.stack = []

    def get_instance():
        if CleaningStack.instance is None:
            CleaningStack.instance = CleaningStack()
        return CleaningStack.instance

    def push(self, col_meta_data, doc, line):
        self.stack.append({'collection': col_meta_data.collection, 'line': line, 'doc': doc})

    def pop(self):
        return self.stack.pop(0)
