import os
import shutil
import _pickle as pickle

from app.services.files_reader import FilesReader
from app.tools.database_context import DatabaseContext
from app.tools.collection_meta_data import CollectionMetaData


class CollectionsSimulator(object):

    def build_single_col(col_name):
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

    def build_big_col(col_name):
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
