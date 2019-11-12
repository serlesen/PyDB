from app.services.file_reader import FileReader
from app.services import file_reader

class SearchService(object):

    def search(self, col_meta_data, search_context):
        return file_reader.find(col_meta_data, search_context)
