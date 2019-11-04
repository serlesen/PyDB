from app.services import file_reader

class CrudService(object):

    def create(self, doc):
        return file_reader.append(doc)

    def update(self, id, doc):
        return file_reader.update(id, doc)

    def delete(self, id):
        return None
