import _pickle as pickle
import os.path
import datetime

from app.services.file_reader import FileReader
from app.tools.database_context import DatabaseContext
from app.tools.filter_tool import FilterTool
from app.tools.search_context import SearchContext

class IndexesService(object):

    INDEX_FILE_NAME = '{}.idx'

    def __init__(self):
        self.file_reader = FileReader()

    def build_index(self, col_meta_data, field):
        docs = self.file_reader.find_all(col_meta_data)
        filter_tool = FilterTool({'$filter': {field: '$exists'}})
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

    def find_all(self, col_meta_data, field, value):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)

        with open(pname, 'rb') as file:
            return pickle.load(file)[value]

    def remove_index(self, col_meta_data, field):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)
        if os.path.exists(pname) is False:
            return {'status': 'missing index'}

        os.remove(pname)
        return col_meta_data.remove_index(field)
