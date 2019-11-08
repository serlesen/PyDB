from app.services.file_reader import FileReader
from app.services import file_reader

class SearchService(object):

    def search(self, collection, search_context):
        return file_reader.find(collection, search_context)
