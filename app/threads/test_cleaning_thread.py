import unittest

from app.services.indexes_service import IndexesService
from app.services.data_service import DataService
from app.services.search_service import SearchService
from app.test.collections_simulator import CollectionsSimulator
from app.threads.cleaning_stack import CleaningStack
from app.threads.cleaning_thread import CleaningThread
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext
from app.tools.filter_tool import FilterTool
from app.tools.search_context import SearchContext

class CleaningThreadTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col', ['id'])

    def setUp(self):
        # instanciate the service to test
        self.cleaning_thread = CleaningThread()
        self.data_service = DataService()
        self.search_service = SearchService()
        self.indexes_service = IndexesService()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def test_clean_deleted_items(self):
        col_meta_data = CollectionMetaData('col')

        count = len(self.data_service.find_all(col_meta_data, None))

        self.data_service.update(col_meta_data, 2, {})
        CleaningStack.get_instance().push(col_meta_data, {}, 1)

        docs = self.data_service.find_all(col_meta_data, None)
        lines = self.indexes_service.find_all(col_meta_data, 'id', FilterTool({'$filter': {'id': 2}}))

        self.assertEqual(len(CleaningStack.get_instance().stack), 1)
        self.assertEqual(count, len(docs))
        self.assertEqual(len(self.search_service.find_in_docs(docs, SearchContext({'$filter': {'id': 2}}))), 0)
        self.assertEqual(len(lines), 1)

        self.cleaning_thread.run()
        
        docs = self.data_service.find_all(col_meta_data, None)
        lines = self.indexes_service.find_all(col_meta_data, 'id', FilterTool({'$filter': {'id': 2}}))

        self.assertEqual(len(CleaningStack.get_instance().stack), 0)
        self.assertEqual(count - 1, len(docs))
        self.assertEqual(len(self.search_service.find_in_docs(docs, SearchContext({'$filter': {'id': 2}}))), 0)
        self.assertEqual(len(lines), 0)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(CleaningThreadTest)
