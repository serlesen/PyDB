import unittest
from app.services.test_collections_service import CollectionsServiceTest
from app.services.test_file_reader import FileReaderTest
from app.services.test_indexes_service import IndexesServiceTest
from app.services.test_search_service import SearchServiceTest
from app.tools.test_filter_tool import FilterToolTest
from app.tools.test_collection_meta_data import CollectionMetaDataTest
from app.tools.test_results_mapper import ResultsMapperTest
from app.tools.test_search_context import SearchContextTest

def suite():
    return unittest.TestSuite([
        CollectionMetaDataTest.suite(),
        CollectionsServiceTest.suite(),
        FileReaderTest.suite(),
        FilterToolTest.suite(),
        IndexesServiceTest.suite(),
        ResultsMapperTest.suite(),
        SearchContextTest.suite(),
        SearchServiceTest.suite()
        ])

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
