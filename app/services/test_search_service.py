import timeout_decorator
import unittest

from app.services.search_service import SearchService
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext
from app.tools.search_context import SearchContext

class SearchServiceTest(unittest.TestCase):

    def setUp(self):
        DatabaseContext.DATA_FOLDER = 'data-test/'
        DatabaseContext.MAX_DOC_PER_FILE = 100000
        self.search_service = SearchService()

    def test_find_doc_in_file(self):
        search_context = SearchContext({'$filter': {'id': 3}})
        results = self.search_service.search(CollectionMetaData('col'), search_context)
        self.assertEqual(len(results), 1)

    def test_find_doc_in_second_file(self):
        search_context = SearchContext({'$filter': {'id': 12}})
        results = self.search_service.search(CollectionMetaData('col'), search_context)
        self.assertEqual(len(results), 1)

    @timeout_decorator.timeout(2.5)
    def test_search_over_250000_docs(self):
        results = self.search_service.search(CollectionMetaData('big-col'), SearchContext({'$filter': {'id': 449994}}))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 449994)

    @timeout_decorator.timeout(1)
    def test_search_over_250000_docs_with_index(self):
        results = self.search_service.search(CollectionMetaData('big-col-with-index'), SearchContext({'$filter': {'id': 449994}}))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 449994)


    def suite():
        return unittest.TestLoader.loadTestsFromTestCase(SearchServiceTest)
