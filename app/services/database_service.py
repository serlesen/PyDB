import os

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.collections_service import CollectionsService
from app.threads.cleaning_stack import CleaningStack
from app.threads.query_stack import QueryStack
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

#
# Class to return a status of the database
#
class DatabaseService(object):

    def __init__(self):
        self.collections_service = DependencyInjectionsService.get_instance().get_service(CollectionsService)

    def get_status(self):
        cols = []
        for f in os.listdir(DatabaseContext.DATA_FOLDER):
            col_meta_data = CollectionMetaData(f)

            cols.append({'collection': f, 'count': self.collections_service.count(col_meta_data), 'size (bytes)': self.collection_size(col_meta_data)})
        return {'collections': cols,
                'cleaning_operations': CleaningStack.get_instance().get_details(),
                'query_operations': QueryStack.get_instance().get_details()
                }

    def collection_size(self, col_meta_data):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(DatabaseContext.DATA_FOLDER + col_meta_data.collection):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)

        return total_size
