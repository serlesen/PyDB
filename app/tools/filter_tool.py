class FilterTool(object):

    def __init__(self, search_filter):
        self.search_filter = search_filter

    def match(self, doc):
        f = self.search_filter['filter']
        return self.match_filter(doc, f)

    def match_filter(self, doc, filter_list):
        if isinstance(filter_list, list):
            return self.match_or(doc, filter_list)
        return self.match_and(doc, filter_list)

    def match_and(self, doc, filter_list):
        for k in filter_list.keys():
            if k == 'filter':
                return self.match_filter(doc, filter_list[k])
            if k not in doc:
                return False
            if isinstance(filter_list[k], list):
                if not self.match_in(doc[k], filter_list[k]):
                    return False
            elif doc[k] != filter_list[k]:
                return False
        return True

    def match_in(self, val, filter_list):
        return val in filter_list

    def match_or(self, doc, filter_list):
        for q in filter_list:
            if self.match_and(doc, q):
                return True
        return False

