class CleaningStack(object):
    """ Stack which contains the cleaning actions.
    A cleaning action is the remove of an empty document after its deletion and the indexes update.
    """

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

    def get_details(self):
        return self.stack

    def contains_data(self):
        return len(self.stack) > 0
