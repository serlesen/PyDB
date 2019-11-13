import os
import shutil

from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CollectionsService(object):

    def create(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection):
            return {'status': 'already existing'}
        os.makedirs(DatabaseContext.DATA_FOLDER + collection)

        # to initialize the meta data of the collection
        CollectionMetaData(collection)

        return {'status': 'done'}

    def create_index(self, collection, field):
        col_meta_data = CollectionMetaData(collection)
        return col_meta_data.add_index(field)

    def remove(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection):
            shutil.rmtree(DatabaseContext.DATA_FOLDER + collection)
            return {'status': 'done'}
        return {'status': 'missing collection'}

    def remove_index(self, collection, field):
        col_meta_data = CollectionMetaData(collection)
        return col_meta_data.remove_index(field)
