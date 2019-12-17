import timeout_decorator
import unittest
import os
import _pickle as pickle

from app.services.data_service import DataService
from app.services.indexes_service import IndexesService
from app.services.search_service import SearchService
from app.test.collections_simulator import CollectionsSimulator
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext
from app.tools.search_context import SearchContext

class SearchServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col', None)
        CollectionsSimulator.build_big_col('big-col', None)
        CollectionsSimulator.build_big_col('big-col-with-index', ['id'])

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def setUp(self):
        self.search_service = SearchService()

    def test_find_doc_in_file(self):
        search_context = SearchContext({'$filter': {'id': 3}})
        results = self.search_service.search_by_thread(CollectionMetaData('col'), search_context, None)
        self.assertEqual(len(results), 1)

    def test_find_doc_in_second_file(self):
        search_context = SearchContext({'$filter': {'id': 6}})
        results = self.search_service.search_by_thread(CollectionMetaData('col'), search_context, None)
        self.assertEqual(len(results), 1)

    def test_find_doc_with_skip_size(self):
        search_context = SearchContext({'$filter': {'first_name': {'$exists': True}}, '$skip': 1, '$size': 2})
        results = self.search_service.search_by_thread(CollectionMetaData('col'), search_context, None)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], 2)
        self.assertEqual(results[1]['id'], 3)

    def test_find_doc_with_skip_size_sort(self):
        search_context = SearchContext({'$filter': {'first_name': {'$exists': True}}, '$skip': 1, '$size': 2, '$sort': {'id': 'DESC'}})
        results = self.search_service.search_by_thread(CollectionMetaData('col'), search_context, None)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], 5)
        self.assertEqual(results[1]['id'], 4)

    def test_find_doc_multiple_sort(self):
        search_context = SearchContext({'$sort': {'first_name': 'ASC', 'last_name': 'DESC'}})
        results = self.search_service.search_by_thread(CollectionMetaData('col'), search_context, None)
        self.assertEqual(len(results), 6)
        self.assertEqual(results[0]['first_name'], 'Biff')
        self.assertEqual(results[1]['first_name'], 'Emmett')
        self.assertEqual(results[2]['first_name'], 'John')
        self.assertEqual(results[2]['last_name'], 'Smith')
        self.assertEqual(results[3]['first_name'], 'John')
        self.assertEqual(results[3]['last_name'], 'Doe')
        self.assertEqual(results[4]['first_name'], 'Marty')
        self.assertEqual(results[5]['first_name'], 'Sergio')

    @timeout_decorator.timeout(2.5)
    def test_search_over_500000_docs(self):
        results = self.search_service.search_by_thread(CollectionMetaData('big-col'), SearchContext({'$filter': {'id': 449994}}), None)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 449994)

    @timeout_decorator.timeout(1)
    def test_search_over_500000_docs_with_index(self):
        results = self.search_service.search_by_thread(CollectionMetaData('big-col-with-index'), SearchContext({'$filter': {'id': 449994}}), None)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 449994)

    @timeout_decorator.timeout(0.5)
    def test_search_over_500000_docs_separated_threads(self):
        results = self.search_service.search_by_thread(CollectionMetaData('big-col'), SearchContext({'$filter': {'id': 449994}}), 5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 449994)

    @timeout_decorator.timeout(1)
    def test_search_over_500000_docs_with_index_separated_threads(self):
        results = self.search_service.search_by_thread(CollectionMetaData('big-col-with-index'), SearchContext({'$filter': {'id': 449994}}), 5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 449994)

    def suite():
        return unittest.TestLoader.loadTestsFromTestCase(SearchServiceTest)
