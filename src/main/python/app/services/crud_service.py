from app.services import file_reader

class CrudService(object):

    def create(self, doc):
        return file_reader.append(doc)

    def bulk_insert(self, docs):
        return file_reader.append_bulk(docs)

    def update(self, id, doc):
        return file_reader.update(id, doc)

    def delete(self, id):
        return None
