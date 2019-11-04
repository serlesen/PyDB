from app.services.file_reader import FileReader
from app.services import file_reader


class SearchService(object):

    def search(self, query):
        key = list(query['filter'].keys())[0]
        return file_reader.find(key, query['filter'][key])
