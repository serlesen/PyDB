import _pickle as pickle
import os.path
import datetime

from app.exceptions.app_exception import AppException
from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.file_reader import FileReader
from app.tools.collection_locker import CollectionLocker, col_locking
from app.tools.database_context import DatabaseContext
from app.tools.filter_tool import FilterTool
from app.tools.search_context import SearchContext

class IndexesService(object):

    INDEX_FILE_NAME = '{}.idx'

    def __init__(self):
        self.file_reader = DependencyInjectionsService.get_instance().get_service(FileReader)

    def enumerate_index_fnames(self, col_meta_data):
       fnames = []
       for i in col_meta_data.indexes.keys():
           fnames.append(self.INDEX_FILE_NAME.format(i))
       return fnames

    @col_locking
    def build_index(self, col_meta_data, field):
        docs = self.file_reader.find_all(col_meta_data)
        filter_tool = FilterTool({'$filter': {field: {'$exists': True}}})
        resulting_docs = []
        for d in docs:
            if filter_tool.match(d):
                resulting_docs.append(d)

        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)
        if os.path.exists(pname):
            return {'status': 'already existing'}

        values = {}
        for i, doc in enumerate(resulting_docs):
            key = doc[field]
            if key not in values:
                values[key] = []
            values[key].append(i)

        with open(pname, 'wb') as file:
            file.write(pickle.dumps(values))

        return col_meta_data.add_index(field, len(resulting_docs))

    def get_line(self, col_meta_data, doc):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format('id')

        with open(pname, 'rb') as file:
            if doc['id'] in values:
                return values[doc['id']]

        raise AppException('Unable to find document with id {}'.format(doc['id']), 400)
        
    @col_locking
    def append_to_indexes(self, col_meta_data, doc, line):
        for field in col_meta_data.indexes.keys():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)

            if field not in doc:
                pass

            CollectionLocker.lock_file(pname)

            with open(pname, 'rb+') as file:
                values = pickle.load(file)
                file.seek(0)
                file.truncate()
                values[value] = line
                file.write(pickle.dumps(values))

            CollectionLocker.unlock_file(pname)

    @col_locking
    def update_indexes(self, col_meta_data, old_doc, new_doc):

        line = self.get_line(col_meta_data, old_doc)

        for field in col_meta_data.indexes.keys():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)

            if field not in old_doc and field not in new_doc:
                pass

            should_remove = True
            if field not in old_doc:
                should_remove = False

            should_add = True
            if field not in new_doc:
                should_add = False

            CollectionLocker.lock_file(pname)

            with open(pname, 'rb+') as file:
                values = pickle.load(file)
                file.seek(0)
                file.truncate()

                if should_remove:
                    values[old_doc[field]].remove(line)

                if should_add:
                    if new_doc[field] not in values:
                        values[new_doc[field]] = []
                    values[new_doc[field]].append(line)

                file.write(pickle.dumps(values))

            CollectionLocker.unlock_file(pname)


    @col_locking
    def find_all(self, col_meta_data, field, filter_tool):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)

        with open(pname, 'rb') as file:
            match_value = filter_tool.search_filter['$filter'][field]
            results = []
            values = pickle.load(file)
            if isinstance(match_value, dict) or isinstance(match_value, list):
                for k in values.keys():
                    if filter_tool.match({field, k}):
                        results.extend(values[k])
            else:
                if match_value in values:
                    results.extend(values[match_value])
            return results

    @col_locking
    def remove_index(self, col_meta_data, field):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)
        if os.path.exists(pname) is False:
            return {'status': 'missing index'}

        os.remove(pname)
        return col_meta_data.remove_index(field)

