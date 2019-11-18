import _pickle as pickle
import os.path

from app.services.search_service import SearchService
from app.tools.database_context import DatabaseContext
from app.tools.search_context import SearchContext

class IndexesService(object):

    INDEX_FILE_NAME = '{}.idx'

    def __init__(self):
        self.search_service = SearchService()

    def build_index(self, col_meta_data, field):
        docs = self.search_service.search(col_meta_data, SearchContext({'$filter': {field: '$exists'}, '$size': -1}))

        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)
        if os.path.exists(pname):
            return {'status': 'already existing'}

        values = {}
        for doc in docs:
            key = doc[field]
            if key not in values:
                values[key] = []
            values[key].append(doc)

        with open(pname, 'wb') as file:
            file.write(pickle.dumps(values))

        return col_meta_data.add_index(field, len(values.keys()))

    def remove_index(self, col_meta_data, field):
        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + self.INDEX_FILE_NAME.format(field)
        if os.path.exists(pname) is False:
            return {'status': 'missing index'}

        os.remove(pname)
        return col_meta_data.remove_index(field)
