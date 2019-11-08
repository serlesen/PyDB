from app.services import file_reader

class CrudService(object):

    def create(self, collection, doc):
        return file_reader.append(collection, doc)

    def bulk_insert(self, collection, docs):
        return file_reader.append_bulk(collection, docs)

    def update(self, collection, id, doc):
        return file_reader.update(collection, id, doc)

    def delete(self, collection, id):
        return file_reader.update(collection, id, None)
