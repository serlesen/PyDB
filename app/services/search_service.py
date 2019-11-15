from app.services.file_reader import FileReader

class SearchService(object):

    def __init__(self):
        self.file_reader = FileReader()

    def search(self, col_meta_data, search_context):
        return self.file_reader.find(col_meta_data, search_context)
