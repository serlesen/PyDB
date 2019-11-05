from app.tools.query_tool import QueryTool

class SearchContext(object):

    def __init__(self, query):
        if 'filter' in query:
            self.filter = QueryTool(query)
        if 'size' in query:
            self.size = query['size']
        if 'skip' in query:
            self.skip = query['skip']
        if 'sort' in query:
            self.sort = query['sort']
        if 'map' in query:
            self.map = query['map']

