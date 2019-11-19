class FilterTool(object):

    def __init__(self, search_filter):
        self.search_filter = search_filter

    def match(self, doc):
        f = self.search_filter['$filter']
        return self.match_filter(doc, f)

    def match_filter(self, doc, filter_list):
        if isinstance(filter_list, list):
            return self.match_or(doc, filter_list)
        return self.match_and(doc, filter_list)

    def match_and(self, doc, filter_list):
        for k in filter_list.keys():
            if k == '$filter':
                return self.match_filter(doc, filter_list[k])
            elif isinstance(filter_list[k], list):
                if not self.match_in(doc[k], filter_list[k]):
                    return False
            elif isinstance(filter_list[k], dict):
                inner_dict_key = list(filter_list[k].keys())[0]
                if inner_dict_key == '$exists':
                    if not self.match_exists(doc, k, filter_list[k][inner_dict_key]):
                        return False
            elif filter_list[k] == '$exists':
                if not self.match_exists(doc, k, True):
                    return False
            elif k not in doc:
                return False
            elif doc[k] != filter_list[k]:
                return False
        return True

    def match_exists(self, doc, field, exists):
        if field in doc and exists:
            return True
        if field not in doc and not exists:
            return True
        return False

    def match_in(self, val, filter_list):
        return val in filter_list

    def match_or(self, doc, filter_list):
        for q in filter_list:
            if self.match_and(doc, q):
                return True
        return False

