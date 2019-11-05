from app.services.file_reader import FileReader
from app.services import file_reader
from app.tools.query_tool import QueryTool

class SearchService(object):

    def search(self, query):
        return file_reader.find(QueryTool(query))
