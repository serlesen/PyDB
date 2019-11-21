import os
import shutil

from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext
from app.services.indexes_service import IndexesService

class CollectionsService(object):

    def __init__(self):
        self.indexes_service = IndexesService()

    def create(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection):
            return {'status': 'already existing'}
        os.makedirs(DatabaseContext.DATA_FOLDER + collection)

        # to initialize the meta data of the collection
        CollectionMetaData(collection)

        # all the collections must have the id index
        return self.indexes_service.build_index(CollectionMetaData(collection), 'id')

    def create_index(self, collection, field):
        return self.indexes_service.build_index(CollectionMetaData(collection), field)

    def remove(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection):
            shutil.rmtree(DatabaseContext.DATA_FOLDER + collection)
            return {'status': 'done'}
        return {'status': 'missing collection'}

    def remove_index(self, collection, field):
        return self.indexes_service.remove_index(CollectionMetaData(collection), field)
