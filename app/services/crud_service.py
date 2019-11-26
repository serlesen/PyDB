import uuid

from app.exceptions.app_exception import AppException
from app.services.file_reader import FileReader
from app.services.search_service import SearchService
from app.tools.search_context import SearchContext

class CrudService(object):

    def __init__(self):
        self.file_reader = FileReader()
        self.search_service = SearchService()

    def create(self, col_meta_data, doc):
        if 'id' not in doc:
            doc['id'] = uuid.uuid4()
        else:
            existing_docs = search_service.search(col_meta_data, SearchContext({'$filter': {'id': doc['id']}, '$size': 1}))
            if len(existing_docs) > 0:
                raise AppException('Document with same ID already in the database', 409)
        return self.file_reader.append(col_meta_data, doc)

    def bulk_insert(self, col_meta_data, docs):
        return self.file_reader.append_bulk(col_meta_data, docs)

    def update(self, col_meta_data, id, doc):
        return self.file_reader.update(col_meta_data, id, doc)

    def delete(self, col_meta_data, id):
        return self.file_reader.update(col_meta_data, id, {})
