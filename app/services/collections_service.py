import os

from app.tools.database_context import DatabaseContext

class CollectionsService(object):

    def create(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection):
            return {'status': 'already existing'}
        os.makedirs(DatabaseContext.DATA_FOLDER + collection)
        return {'status': 'done'}

    def remove(self, collection):
        if os.path.exists(DatabaseContext.DATA_FOLDER + collection):
            os.rmdir(DatabaseContext.DATA_FOLDER + collection)
            return {'status': 'done'}
        return {'status': 'missing collection'}
