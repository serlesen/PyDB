import uuid

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.exceptions.app_exception import AppException
from app.services.collections_service import CollectionsService
from app.services.file_reader import FileReader
from app.services.indexes_service import IndexesService
from app.services.search_service import SearchService
from app.tools.search_context import SearchContext
from app.threads.cleaning_stack import CleaningStack

class CrudService(object):

    def __init__(self):
        self.collections_service = DependencyInjectionsService.get_instance().get_service(CollectionsService)
        self.file_reader = DependencyInjectionsService.get_instance().get_service(FileReader)
        self.indexes_service = DependencyInjectionsService.get_instance().get_service(IndexesService)
        self.search_service = DependencyInjectionsService.get_instance().get_service(SearchService)

    def create(self, col_meta_data, doc):
        if 'id' not in doc:
            doc['id'] = uuid.uuid4()
        else:
            existing_docs = search_service.search(col_meta_data, SearchContext({'$filter': {'id': doc['id']}, '$size': 1}))
            if len(existing_docs) > 0:
                raise AppException('Document with same ID already in the database', 409)
        updated = self.file_reader.append(col_meta_data, doc)
        appended_line = self.collections_service.count(col_meta_data) - 1
        self.indexes_service.append_to_index(col_meta_data, doc, appended_line)
        return updated

    def bulk_insert(self, col_meta_data, docs):
        return self.file_reader.append_bulk(col_meta_data, docs)

    def update(self, col_meta_data, id, doc):
        previous_docs = self.search_service.search(col_meta_data, SearchContext({'$filter': {'id': id}, '$size': 1}))
        if len(previous_docs) != 1:
            raise AppException('Unable to update document with id {}'.format(id), 400)
        self.indexes_service.update_indexes(col_meta_data, previous_docs[0], doc)
        return self.file_reader.update(col_meta_data, id, doc)['doc']

    def delete(self, col_meta_data, id):
        deleted_doc = self.file_reader.update(col_meta_data, id, {})
        CleaningStack.get_instance().push(col_meta_data, deleted_doc['doc'], deleted_doc['line'])
        return deleted_doc['doc']
