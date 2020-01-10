import unittest

from app.services.collections_service import CollectionsService
from app.services.crud_service import CrudService
from app.services.files_reader import FilesReader
from app.services.indexes_service import IndexesService
from app.services.query_manager import QueryManager
from app.test.collections_simulator import CollectionsSimulator
from app.threads.threads_manager import ThreadsManager
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CrudServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if DatabaseContext.THREADS_MANAGER_CYCLING == False:
            DatabaseContext.THREADS_MANAGER_CYCLING = True
            ThreadsManager().start()

        CollectionsSimulator.build_single_col('col', ['id'])

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def setUp(self):
        self.crud_service = CrudService()
        self.collections_service = CollectionsService()
        self.query_manager = QueryManager()
        self.indexes_service = IndexesService()

    def test_bulk_insert_new_docs(self):
        docs = [{'id': 11}, {'id': 12}, {'id': 13}, {'id': 14}, {'id': 15}]
        col_meta_data = CollectionMetaData('col')

        count = self.collections_service.count(col_meta_data)

        self.crud_service.bulk_upsert(col_meta_data, docs)

        self.assertEqual(self.collections_service.count(col_meta_data), count + 5)
        self.assertEqual(self.indexes_service.get_lines(col_meta_data, 11), [count])
        self.assertEqual(self.indexes_service.get_lines(col_meta_data, 12), [count + 1])
        self.assertEqual(self.indexes_service.get_lines(col_meta_data, 13), [count + 2])
        self.assertEqual(self.indexes_service.get_lines(col_meta_data, 14), [count + 3])
        self.assertEqual(self.indexes_service.get_lines(col_meta_data, 15), [count + 4])
        
    def test_bulk_update_docs(self):
        docs = [{'id': 2, 'first_name': 'Joe', 'last_name': 'Smith'}, {'id': 5, 'first_name': 'Emmetttttttt', 'last_name': 'Brown'}]
        col_meta_data = CollectionMetaData('col')

        count = self.collections_service.count(col_meta_data)

        self.crud_service.bulk_upsert(col_meta_data, docs)

        self.assertEqual(self.collections_service.count(col_meta_data), count)

        self.assertEqual(self.query_manager.get_one(col_meta_data.collection, 2), docs[0])
        self.assertEqual(self.query_manager.get_one(col_meta_data.collection, 5), docs[1])

    def test_bulk_insert_and_update(self):
        docs = [{'id': 21}, {'id': 2, 'first_name': 'Jack', 'last_name': 'Smith'}, {'id': 22}, {'id': 5, 'first_name': 'Emmmmmmmmmmmmmet', 'last_name': 'Brown'}, {'id': 23}]
        col_meta_data = CollectionMetaData('col')

        count = self.collections_service.count(col_meta_data)

        self.crud_service.bulk_upsert(col_meta_data, docs)

        self.assertEqual(self.collections_service.count(col_meta_data), count + 3)
        self.assertEqual(self.query_manager.get_one(col_meta_data.collection, 2), docs[1])
        self.assertEqual(self.query_manager.get_one(col_meta_data.collection, 5), docs[3])
        self.assertEqual(self.indexes_service.get_lines(col_meta_data, 21), [count])
        self.assertEqual(self.indexes_service.get_lines(col_meta_data, 22), [count + 1])
        self.assertEqual(self.indexes_service.get_lines(col_meta_data, 23), [count + 2])

    def test_bulk_delete(self):
        search_query = {'$filter': {'id': [3, 4]}}
        col_meta_data = CollectionMetaData('col')

        self.crud_service.bulk_delete(col_meta_data, search_query)

        results = self.query_manager.search(col_meta_data.collection, search_query)
        self.assertEqual(len(results), 0)

    def suite():
        return unittest.TestLoader.loadTestsFromTestCase(SearchServiceTest)
