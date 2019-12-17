import os
import shutil
import _pickle as pickle

from app.services.data_service import DataService
from app.services.indexes_service import IndexesService
from app.services.files_reader import FilesReader
from app.tools.database_context import DatabaseContext
from app.tools.collection_meta_data import CollectionMetaData


class CollectionsSimulator(object):

    def build_users_col():
        # don't override MAX_DOC_PER_FILE, use the previous one
        col_meta_data = CollectionsSimulator.init_data_folder('users', DatabaseContext.MAX_DOC_PER_FILE)

        docs = []
        docs.append({'id': 1, 'login': 'admin', 'password': '$2b$13$qG6c01Xy9rd07vJ1lZsxE.ouYvdhbFVAn/miQBhnOXq5bk..4WhCC', 'role': 'admin', 'permissions': {}, 'tokens': ['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzU5OTEwNDUsInN1YiI6MX0._jTMkfDl2RKzY_r6nUDVwFG8xlEuZPFFr7zvqWXJmcM']})
        docs.append({'id': 2, 'login': 'replicator', 'password': '', 'role': 'replicator', 'permissions': {}, 'tokens': ['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTExNTksInN1YiI6Mn0.Uf2tyw4vPxKQ95id2iOefp4GcO3UGnYXZLPyX8NoV1U']})
        docs.append({'id': 3, 'login': 'editor', 'password': '$2b$13$0WXjchCmXzA.LSDJ.VFY3e3236N8OYuhzxgxK/CGLKZlvObIKnVXK', 'role': 'editor', 'permissions': {}, 'tokens': ['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6M30.KdhWBZg9yzN7CI80242mnsBKV3js_e-bhgICR8yb82o']})
        docs.append({'id': 4, 'login': 'user', 'password': '$2b$13$..pzR.sYdfI0i4qwSgHBfuXetDpOLru4iGo4ia1qxj4RahEalTnXS', 'role': 'user', 'permissions': {'col': 'w'}, 'tokens': ['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzY1OTIwNTcsInN1YiI6NH0.DdyUZYKPqpFtkfwCIZgI-H4da0Ux4H4yxvlCbHxOIyE']})

        length = len(docs)
        docs_to_write = []
        for i in range(length):
            with open(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname(), 'ab') as file:
                docs_to_write.append(docs.pop(0))
                if (i + 1) == DatabaseContext.MAX_DOC_PER_FILE or len(docs) == 0:
                    file.write(pickle.dumps(docs_to_write))
                    docs_to_write = []
                    if len(docs) > 0:
                        col_meta_data.next_data_fname()


        for field in ['id', 'login']:
            CollectionsSimulator.build_indexes(col_meta_data, field)

    def build_single_col(col_name, indexes):
        col_meta_data = CollectionsSimulator.init_data_folder(col_name, 3)

        # set up the test data
        with open(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.last_data_fname(), 'wb') as file:
            docs = []
            docs.append({'id': 1, 'first_name': 'John', 'last_name': 'Doe'})
            docs.append({'id': 2, 'first_name': 'John', 'last_name': 'Smith'})
            docs.append({'id': 3, 'first_name': 'Sergio', 'last_name': 'Lema'})
            file.write(pickle.dumps(docs))

        with open(DatabaseContext.DATA_FOLDER + col_meta_data.collection + '/' + col_meta_data.next_data_fname(), 'wb') as file:
            docs = []
            docs.append({'id': 4, 'first_name': 'Marty', 'last_name': 'McFly'})
            docs.append({'id': 5, 'first_name': 'Emmett', 'last_name': 'Brown'})
            docs.append({'id': 6, 'first_name': 'Biff', 'last_name': 'Tannen'})
            file.write(pickle.dumps(docs))

        if indexes is not None:
            for field in indexes:
                CollectionsSimulator.build_indexes(col_meta_data, field)

    def build_big_col(col_name, indexes):
        big_col_meta_data = CollectionsSimulator.init_data_folder(col_name, 100000)

        # set up the test data
        for i in range(5):
            with open(DatabaseContext.DATA_FOLDER + big_col_meta_data.collection + '/' + big_col_meta_data.last_data_fname(), 'wb') as file:
                docs = []
                for j in range(DatabaseContext.MAX_DOC_PER_FILE):
                    docs.append({"id": ((i*DatabaseContext.MAX_DOC_PER_FILE)+j),
                         "first_name": "al",
                         "last_name": "jym",
                         "age": 15,
                         "address": "somewhere",
                         "job": "something",
                         "salary": 15352,
                         "email": "my.email@google.com"
                        })
                file.write(pickle.dumps(docs))
                if i != 4:
                    big_col_meta_data.next_data_fname()

        if indexes is not None:
            for field in indexes:
                CollectionsSimulator.build_indexes(big_col_meta_data, field)

    def build_indexes(col_meta_data, field):
        indexes_service = IndexesService()
        data_service = DataService()
        docs = data_service.find_all(col_meta_data, None)
        indexes_service.build_index(col_meta_data, docs, field)

    def init_data_folder(col_name, col_size):
        DatabaseContext.MAX_DOC_PER_FILE = col_size
        DatabaseContext.DATA_FOLDER = 'data-test/'

        if os.path.exists(DatabaseContext.DATA_FOLDER) == False:
            os.makedirs(DatabaseContext.DATA_FOLDER)

        if os.path.exists(DatabaseContext.DATA_FOLDER + col_name) == False:
            os.makedirs(DatabaseContext.DATA_FOLDER + col_name)

        return CollectionMetaData(col_name)

    def clean():
        shutil.rmtree(DatabaseContext.DATA_FOLDER)
        FilesReader.get_instance().reset()
