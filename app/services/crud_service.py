from app.services import file_reader

class CrudService(object):

    def create(self, col_meta_data, doc):
        return file_reader.append(col_meta_data, doc)

    def bulk_insert(self, col_meta_data, docs):
        return file_reader.append_bulk(col_meta_data, docs)

    def update(self, col_meta_data, id, doc):
        return file_reader.update(col_meta_data, id, doc)

    def delete(self, col_meta_data, id):
        return file_reader.update(col_meta_data, id, None)
