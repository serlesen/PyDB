import os
import shutil

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.data_service import DataService
from app.services.indexes_service import IndexesService
from app.tools.collection_locker import col_locking
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CollectionsService(object):
    """ Class to create and remove a collection. It also returns some meta data about a collections as the count. """

    def __init__(self):
        self.indexes_service = DependencyInjectionsService.get_instance().get_service(IndexesService)
        self.data_service = DependencyInjectionsService.get_instance().get_service(DataService)

    def get_status(self, collection):
        col_meta_data = CollectionMetaData(collection)

        indexes = []
        for k in col_meta_data.indexes.keys():
            indexes.append({'field': k, 'count': col_meta_data.indexes[k]})

        return {'count' : self.count(col_meta_data),
                'indexes': indexes
                }

    @col_locking
    def count(self, col_meta_data):
        count = (col_meta_data.counter - 1) * DatabaseContext.MAX_DOC_PER_FILE
        count += self.data_service.file_len(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname())
        return count

    def create(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection):
            return {'status': 'already existing'}
        os.makedirs(DatabaseContext.DATA_FOLDER + collection)

        # to initialize the meta data of the collection
        CollectionMetaData(collection)

        # all the collections must have the id index
        return self.indexes_service.build_index(CollectionMetaData(collection), [], 'id')

    def remove(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection):
            shutil.rmtree(DatabaseContext.DATA_FOLDER + collection)
            return {'status': 'done'}
        return {'status': 'missing collection'}

