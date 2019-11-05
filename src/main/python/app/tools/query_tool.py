class QueryTool(object):

    def __init__(self, query):
        self.query = query

    def match(self, doc):
        f = self.query['filter']
        return self.match_filter(doc, f)

    def match_filter(self, doc, query_list):
        if isinstance(query_list, list):
            return self.match_or(doc, query_list)
        return self.match_and(doc, query_list)

    def match_and(self, doc, query_list):
        for k in query_list.keys():
            if k == 'filter':
                return self.match_filter(doc, query_list[k])
            if k not in doc:
                return False
            if isinstance(query_list[k], list):
                if not self.match_in(doc[k], query_list[k]):
                    return False
            elif doc[k] != query_list[k]:
                return False
        return True

    def match_in(self, val, query_list):
        return val in query_list

    def match_or(self, doc, query_list):
        for q in query_list:
            if self.match_and(doc, q):
                return True
        return False

