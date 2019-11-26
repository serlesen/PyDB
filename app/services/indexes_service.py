import _pickle as pickle
import os.path
import datetime

from app.services.file_reader import FileReader
from app.tools.database_context import DatabaseContext
from app.tools.filter_tool import FilterTool
from app.tools.search_context import SearchContext

class IndexesService(object):

    INDEX_FILE_NAME = '{}.idx'
    LOCK_FILE = '{}.lock'

    def __init__(self):
        self.file_reader = FileReader()

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

    def append_to_indexes(self, col_meta_data, doc, line):
        for field in col_meta_data.indexes.keys():
            pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)

            if field not in doc:
                pass

            self.lock_file(pname)

            with open(pname, 'rb+') as file:
                values = pickle.load(file)
                file.seek(0)
                file.truncate()
                values[value] = line
                file.write(pickle.dumps(values))

            self.unlock_file(pname)

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

    def remove_index(self, col_meta_data, field):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)
        if os.path.exists(pname) is False:
            return {'status': 'missing index'}

        os.remove(pname)
        return col_meta_data.remove_index(field)

    def lock_file(self, pname):
        while os.path.exists(self.LOCK_FILE.format(pname)):
            time.sleep(0.01)

        with open(self.LOCK_FILE.format(pname), 'w') as file:
            file.write('x')

    def unlock_file(self, pname):
        os.remove(self.LOCK_FILE.format(pname))
