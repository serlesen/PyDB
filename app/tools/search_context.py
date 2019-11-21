from app.tools.filter_tool import FilterTool
from app.tools.database_context import DatabaseContext

class SearchContext(object):

    def __init__(self, raw_auery):
        query = {}
        for k in raw_query.keys():
            query[k.lower()] = raw_query[k]

        if '$filter' in query:
            self.filter = FilterTool(query)
            self.filter_keys = []
            for k in query['$filter'].keys():
                self.filter_keys.append({k: query['$filter'][k]})
        else:
            self.filter = None

        if '$size' in query:
            self.size = query['$size']
        else:
            self.size = DatabaseContext.DEFAULT_RESULTS_SIZE

        if '$skip' in query:
            self.skip = query['$skip']
        else:
            self.skip = DatabaseContext.DEFAULT_RESULTS_SKIP

        if '$sort' in query:
            self.sort = query['$sort']
        else:
            self.sort = DatabaseContext.DEFAULT_RESULTS_SORT

        if '$map' in query:
            self.map = query['$map']
        else:
            self.map = None

