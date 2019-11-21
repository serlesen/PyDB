from app.services.file_reader import FileReader

class CrudService(object):

    def __init__(self):
        self.file_reader = FileReader()

    def create(self, col_meta_data, doc):
        return self.file_reader.append(col_meta_data, doc)

    def bulk_insert(self, col_meta_data, docs):
        return self.file_reader.append_bulk(col_meta_data, docs)

    def update(self, col_meta_data, id, doc):
        return self.file_reader.update(col_meta_data, id, doc)

    def delete(self, col_meta_data, id):
        return self.file_reader.update(col_meta_data, id, {})
