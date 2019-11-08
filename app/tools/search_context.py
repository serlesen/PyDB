from app.tools.filter_tool import FilterTool

class SearchContext(object):

    def __init__(self, query):
        if 'filter' in query:
            self.filter = FilterTool(query)
        else:
            self.filter = None

        if 'size' in query:
            self.size = query['size']
        else:
            self.size = 10

        if 'skip' in query:
            self.skip = query['skip']
        else:
            self.skip = 0

        if 'sort' in query:
            self.sort = query['sort']
        else:
            self.sort = None

        if 'map' in query:
            self.map = query['map']
        else:
            self.map = None

