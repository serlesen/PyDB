import timeout_decorator
import unittest

from app.services.search_service import SearchService
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext
from app.tools.search_context import SearchContext

class SearchServiceTest(unittest.TestCase):

    def setUp(self):
        DatabaseContext.DATA_FOLDER = 'data-test/'
        self.search_service = SearchService()

    @timeout_decorator.timeout(1.5)
    def test_search_over_250000_docs(self):
        self.search_service.search(CollectionMetaData('big-col'), SearchContext({'$filter': {'id': 249994}}))

    def suite():
        return unittest.TestLoader.loadTestsFromTestCase(SearchServiceTest)
