import datetime

from app.services.file_reader import FileReader
from app.services.indexes_service import IndexesService

class SearchService(object):

    def __init__(self):
        self.file_reader = FileReader()
        self.indexes_service = IndexesService()

    def search(self, col_meta_data, search_context):
        indexed_value = self.find_field_in_index(col_meta_data, search_context)
        if indexed_value != None:
            k = list(indexed_value.keys())[0]
            v = indexed_value[k]
            lines = self.indexes_service.find_all(col_meta_data, k, v)
            docs = self.file_reader.find_by_line(col_meta_data, lines)
            res = self.find_in_docs(docs, search_context)
            return res
        docs = self.file_reader.find_all(col_meta_data)
        return self.find_in_docs(docs, search_context)

    def find_field_in_index(self, col_meta_data, search_context):
        best_indexed_value = None
        for indexed_value in search_context.filter_keys:
            k = list(indexed_value.keys())[0]
            if k in col_meta_data.indexes:
                if best_indexed_value == None:
                    best_indexed_value = indexed_value
                elif col_meta_data.indexes[best_indexed_value] < col_meta_data.indexes[indexed_value]:
                    best_indexed_value = indexed_value
        return best_indexed_value

    def find_in_docs(self, docs, search_context):
            results = []
            for doc in docs:
                if search_context.filter.match(doc):
                    results.append(doc)
                    if len(results) == search_context.size:
                        return results
            return results
