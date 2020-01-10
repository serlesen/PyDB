import re

class FilterTool(object):
    """ Class which handle the logic to filter a document. """

    def __init__(self, search_filter):
        self.search_filter = search_filter

    def match(self, doc):
        if not doc:
            return False
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
            elif k == '$not':
                return not self.match_filter(doc, filter_list[k])
            elif '.' in k:
                if not self.match_inner_doc(doc, k, filter_list):
                    return False
            elif isinstance(filter_list[k], list):
                if not self.match_in(doc[k], filter_list[k]):
                    return False
            elif isinstance(filter_list[k], dict):
                if not self.match_inner_dict(doc, k, filter_list[k]):
                    return False
            elif k not in doc:
                return False
            elif isinstance(doc[k], list):
                if not self.match_in_list(doc[k], filter_list[k]):
                    return False
            elif doc[k] != filter_list[k]:
                return False
        return True

    def match_inner_doc(self, doc, field_def, filter_list):
        fields = field_def.split('.')
        inner_doc = doc
        last_key = fields[0]
        for f in fields:
            if f in inner_doc:
                inner_doc = inner_doc[f]
                last_key = f
            else:
                return False
        return self.match_filter({last_key :inner_doc}, {last_key : filter_list[field_def]})

    def match_inner_dict(self, doc, field, inner_dict):
        inner_dict_key = list(inner_dict.keys())[0]
        if inner_dict_key == '$exists':
            if not self.match_exists(doc, field, inner_dict[inner_dict_key]):
                return False
        elif inner_dict_key in ['$gt', '$lt', '$gte', '$lte']:
            if not self.match_comparison(doc, field, inner_dict[inner_dict_key], inner_dict_key):
                return False
        elif inner_dict_key == '$reg':
            if not self.match_regex(doc, field, inner_dict[inner_dict_key]):
                return False
        elif inner_dict_key == '$not':
            return doc[field] != inner_dict[inner_dict_key]
        return True

    def match_regex(self, doc, field, regex):
        if re.match(regex, doc[field]):
            result = re.match(regex, doc[field])
            return True
        return False

    def match_comparison(self, doc, field, val, comparison):
        if field not in doc:
            return False
        if comparison == '$gt':
            return doc[field] > val
        if comparison == '$lt':
            return doc[field] < val
        if comparison == '$gte':
            return doc[field] >= val
        if comparison == '$lte':
            return doc[field] <= val
        return False

    def match_exists(self, doc, field, exists):
        if field in doc and exists:
            return True
        return field not in doc and not exists

    def match_in(self, val, filter_list):
        return val in filter_list

    def match_in_list(self, doc_list, filter_val):
        return filter_val in doc_list

    def match_or(self, doc, filter_list):
        for q in filter_list:
            if self.match_and(doc, q):
                return True
        return False

