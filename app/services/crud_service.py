import uuid

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.exceptions.app_exception import AppException
from app.services.collections_service import CollectionsService
from app.services.data_service import DataService
from app.services.indexes_service import IndexesService
from app.services.query_manager import QueryManager
from app.tools.search_context import SearchContext
from app.threads.cleaning_stack import CleaningStack

class CrudService(object):
    """ Class to create, update and delete a single document. """

    def __init__(self):
        self.collections_service = DependencyInjectionsService.get_instance().get_service(CollectionsService)
        self.data_service = DependencyInjectionsService.get_instance().get_service(DataService)
        self.indexes_service = DependencyInjectionsService.get_instance().get_service(IndexesService)
        self.query_manager = DependencyInjectionsService.get_instance().get_service(QueryManager)

    def upsert(self, col_meta_data, doc):
        previous_doc = self.query_manager.get_one(col_meta_data.collection, doc['id'])
        if previous_doc is None:
            updated = self.data_service.append(col_meta_data, [doc])
            appended_line = self.collections_service.count(col_meta_data) - 1
            self.indexes_service.append_to_indexes(col_meta_data, doc, appended_line)
            return updated[0]
        else:
            self.indexes_service.update_indexes(col_meta_data, previous_doc, doc)
            return self.data_service.update(col_meta_data, doc['id'], doc)['doc']

    def bulk_upsert(self, col_meta_data, docs):
        return self.data_service.append(col_meta_data, docs)

    def delete(self, col_meta_data, id):
        deleted_doc = self.data_service.update(col_meta_data, id, {})
        CleaningStack.get_instance().push(col_meta_data, deleted_doc['doc'], deleted_doc['line'])
        return deleted_doc['doc']
