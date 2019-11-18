import unittest

from app.services.indexes_service import IndexesService
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class IndexesServiceTest(unittest.TestCase):

    def setUp(self):
        DatabaseContext.DATA_FOLDER = 'data-test/'
        self.indexes_service = IndexesService()

    def test_create_index(self):
        col_meta_data = CollectionMetaData('col')

        result = self.indexes_service.build_index(col_meta_data, 'id')

        self.assertEqual(result['status'], 'done')

    def test_remove_index(self):
        col_meta_data = CollectionMetaData('col')

        result = self.indexes_service.remove_index(col_meta_data, 'id')

        self.assertEqual(result['status'], 'done')


    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(IndexesServiceTest) 
