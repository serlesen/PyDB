import os.path

from app.services.search_service import SearchService

class IndexesService(object):

    INDEX_FILE_NAME = '{}.idx'

    def __init__(self):
        self.search_service = SearchService()

    def build_index(self, col_meta_data, field):
        docs = self.search_service.search(col_meta_data, SearchContext({'$filter': {}}))

        pname = DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + INDEX_FILE_NAME.format(field)
        if os.path.exists(pname):
            return {'status': 'already existing'}

        with open(pname, 'wb') as file:
            pass

        return col_meta_data.add_index(field)

    def remove_index(self, col_meta_data, field):
        return col_meta_data.remove_index(field)
