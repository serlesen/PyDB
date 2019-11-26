class SortTool(object):

    def __init__(self, sort_dict):
        self.sort_dict = sort_dict

    def get_sort_attributes(self):
        attributes = []
        for k in self.sort_dict.keys():
            attributes.append({'key': k, 'reverse': self.sort_dict[k] == 'DESC'})
        return attributes

