import _pickle as pickle
import os.path

from app.exceptions.app_exception import AppException
from app.services.files_reader import FilesReader
from app.tools.collection_locker import CollectionLocker, col_locking
from app.tools.database_context import DatabaseContext
from app.tools.filter_tool import FilterTool
from app.tools.search_context import SearchContext

class IndexesService(object):
    """ Class to create, remove and update the indexes. It also searches into the indexes content. """

    @col_locking
    def build_index(self, col_meta_data, docs, field):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.get_index_fname(field)
        if os.path.exists(pname):
            return {'status': 'already existing'}

        filter_tool = FilterTool({'$filter': {field: {'$exists': True}}})
        resulting_docs = []
        for d in docs:
            if filter_tool.match(d):
                resulting_docs.append(d)

        values = {}
        for i, doc in enumerate(resulting_docs):
            key = doc[field]
            if key not in values:
                values[key] = []
            values[key].append(i)

        with open(pname, 'wb') as file:
            file.write(pickle.dumps(values))
        FilesReader.get_instance().invalidate_file_content(pname)

        return col_meta_data.add_or_update_index_count(field, len(resulting_docs))

    def get_lines(self, col_meta_data, id):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.get_index_fname('id')

        values = FilesReader.get_instance().get_file_content(pname)
        if id in values:
            return values[id]

        raise AppException('Unable to find document with id {}'.format(id), 400)
        
    @col_locking
    def append_to_indexes(self, col_meta_data, docs, first_line):
        for field in col_meta_data.indexes.keys():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.get_index_fname(field)

            values = None
            for idx, doc in enumerate(docs):
                if field not in doc:
                    pass
    
                if values is None:
                    values = FilesReader.get_instance().get_file_content(pname)
    
                v = doc[field]
                if v not in values:
                    values[v] = []
                values[v].append(first_line + idx)

            if values is not None:
                FilesReader.get_instance().write_file_content(pname, values)

    @col_locking
    def update_indexes(self, col_meta_data, old_docs, new_docs):

        for field in col_meta_data.indexes.keys():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.get_index_fname(field)
            
            old_docs_it = iter(old_docs)
            new_docs_it = iter(new_docs)
            
            values = None
            try:
                while True:
                    old_doc = next(old_docs_it)
                    new_doc = next(new_docs_it)

                    if field not in old_doc and field not in new_doc:
                        pass
    
                    # remove from the index the value of the old document
                    should_remove = True
                    if field not in old_doc:
                        should_remove = False
    
                    # add to the index the value of the new document
                    should_add = True
                    if field not in new_doc:
                        should_add = False
    
                    # copy the list as it will be modified later
                    lines = list(self.get_lines(col_meta_data, old_doc['id']))
                    
                    if values is None:
                        values = FilesReader.get_instance().get_file_content(pname)

                    if should_remove:
                        values[old_doc[field]] = list(set(values[old_doc[field]]) - set(lines))
                    
                    if should_add:
                        if new_doc[field] not in values:
                            values[new_doc[field]] = []
                        values[new_doc[field]].extend(lines)
    
            except StopIteration:
                if values is not None:
                    FilesReader.get_instance().write_file_content(pname, values)

    @col_locking
    def find_all(self, col_meta_data, field, filter_tool):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.get_index_fname(field)

        match_value = filter_tool.search_filter['$filter'][field]
        results = []
        values = FilesReader.get_instance().get_file_content(pname)
        if isinstance(match_value, dict) or isinstance(match_value, list):
            for k in values.keys():
                if filter_tool.match({field: k}):
                    results.extend(values[k])
        else:
            if match_value in values:
                results.extend(values[match_value])
        return results

    @col_locking
    def remove_index(self, col_meta_data, field):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.get_index_fname(field)
        if os.path.exists(pname) is False:
            return {'status': 'missing index'}

        os.remove(pname)
        return col_meta_data.remove_index_count(field)

