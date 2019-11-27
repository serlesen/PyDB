import os
import shutil

from app.services.file_reader import FileReader
from app.services.indexes_service import IndexesService
from app.tools.collection_locker import col_locking
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CollectionsService(object):

    def __init__(self):
        self.indexes_service = IndexesService()
        self.file_reader = FileReader()

    def get_status(self, collection):
        col_meta_data = CollectionMetaData(collection)

        indexes = []
        for k in col_meta_data.indexes.keys():
            indexes.append({'field': k, 'count': col_meta_data.indexes[k]})

        return {'count' : self.count(col_meta_data),
                'indexes': indexes}

    @col_locking
    def count(self, col_meta_data):
        count = (col_meta_data.counter - 1) * DatabaseContext.MAX_DOC_PER_FILE
        count += self.file_reader.file_len(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname())
        return count

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
