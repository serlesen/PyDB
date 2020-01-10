import uuid
from operator import itemgetter

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
            self.indexes_service.append_to_indexes(col_meta_data, [doc], appended_line)
            return updated[0]
        else:
            return self.patch(col_meta_data, [previous_doc], [doc])[0]['doc']

    def patch(self, col_meta_data, previous_docs, docs):
        # sort the lists, as the elements are read by an iterator
        previous_docs = sorted(previous_docs, key=itemgetter('id'))
        docs = sorted(docs, key=itemgetter('id'))
        ids = sorted(list(map(lambda d: d['id'], previous_docs)))

        self.indexes_service.update_indexes(col_meta_data, previous_docs, docs)
        return self.data_service.update(col_meta_data, ids, docs)

    def bulk_upsert(self, col_meta_data, docs):
        ids = list(map(lambda d: d['id'], docs)) 

        updated_docs = []

        existing_docs = self.query_manager.search(col_meta_data.collection, {'$filter': {'id': ids}})
        ids = list(map(lambda d: d['id'], existing_docs))

        new_docs = []
        updating_docs = []
        for d in docs:
            if d['id'] in ids:
                updating_docs.append(d)
            else:
                new_docs.append(d)

        if len(updating_docs) > 0:
            results = self.patch(col_meta_data, existing_docs, updating_docs)
            updated_docs.extend(list(map(lambda r: r['doc'], results)))

        if len(new_docs) > 0:
            updated_docs.extend(self.data_service.append(col_meta_data, new_docs))
            appended_lines = self.collections_service.count(col_meta_data) - len(new_docs)
            self.indexes_service.append_to_indexes(col_meta_data, new_docs, appended_lines)

        return updated_docs


    def delete(self, col_meta_data, id):
        deleted_doc = self.data_service.update(col_meta_data, [id], [{}])[0]
        CleaningStack.get_instance().push(col_meta_data, deleted_doc['doc'], deleted_doc['line'])
        return deleted_doc['doc']

    def bulk_delete(self, col_meta_data, search_query):
        docs = self.query_manager.search(col_meta_data.collection, search_query)
        ids = sorted(list(map(lambda d: d['id'], docs)))

        empty_docs = []
        for i in ids:
            empty_docs.append({})

        deleted_docs = self.data_service.update(col_meta_data, ids, empty_docs)
        for deleted_doc in deleted_docs:
            CleaningStack.get_instance().push(col_meta_data, deleted_doc['doc'], deleted_doc['line'])
