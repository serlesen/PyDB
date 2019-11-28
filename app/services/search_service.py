import datetime

from operator import itemgetter

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.file_reader import FileReader
from app.services.indexes_service import IndexesService
from app.tools.filter_tool import FilterTool

class SearchService(object):

    def __init__(self):
        self.file_reader = DependencyInjectionsService.get_instance().get_service(FileReader)
        self.indexes_service = DependencyInjectionsService.get_instance().get_service(IndexesService)

    def search(self, col_meta_data, search_context):
        indexed_value = self.find_field_in_index(col_meta_data, search_context)
        if indexed_value != None:
            k = list(indexed_value.keys())[0]
            lines = self.indexes_service.find_all(col_meta_data, k, FilterTool({'$filter': indexed_value}))
            docs = self.file_reader.find_by_line(col_meta_data, lines)
            res = self.find_in_docs(docs, search_context)
            return res
        docs = self.file_reader.find_all(col_meta_data)
        return self.find_in_docs(docs, search_context)

    def find_field_in_index(self, col_meta_data, search_context):
        if search_context.filter is None:
            return None

        best_indexed_value = None
        best_indexed_value_count = 0
        for indexed_value in search_context.filter_keys:
            k = list(indexed_value.keys())[0]
            if k in col_meta_data.indexes:
                if best_indexed_value == None:
                    best_indexed_value = indexed_value
                    best_indexed_value_count = col_meta_data.indexes[k]
                elif best_indexed_value_count < col_meta_data.indexes[k]:
                    best_indexed_value = indexed_value
                    best_indexed_value_count = col_meta_data.indexes[k]
        return best_indexed_value

    def find_in_docs(self, docs, search_context):
        results = []
        if search_context.filter is not None:
            for doc in docs:
                if search_context.filter.match(doc):
                    results.append(doc)
                    if search_context.sort == None and len(results) == search_context.size + search_context.skip:
                        return results[search_context.skip:search_context.skip + search_context.size]
        else:
            results = docs
        return self.sort_and_limit_results(results, search_context)

    def sort_and_limit_results(self, results, search_context):
        if search_context.sort != None:
            sort_attributes = search_context.sort.get_sort_attributes()
            for s in reversed(sort_attributes):
                results = sorted(results, key=itemgetter(s['key']), reverse=s['reverse'])
        return results[search_context.skip:search_context.skip + search_context.size]
        
