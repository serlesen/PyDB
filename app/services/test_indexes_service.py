import unittest
import os
import _pickle as pickle

from app.services.indexes_service import IndexesService
from app.test.collections_simulator import CollectionsSimulator
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext
from app.tools.filter_tool import FilterTool

class IndexesServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col')

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def setUp(self):
        self.indexes_service = IndexesService()

    def test_create_index(self):
        col_meta_data = CollectionMetaData('col')

        result = self.indexes_service.build_index(col_meta_data, 'id')

        self.assertEqual(result['status'], 'done')

    def test_remove_index(self):
        col_meta_data = CollectionMetaData('col')

        result = self.indexes_service.remove_index(col_meta_data, 'id')

        self.assertEqual(result['status'], 'done')

    def test_update_indexes(self):
        col_meta_data = CollectionMetaData('col')
        self.indexes_service.build_index(col_meta_data, 'id')

        lines = self.indexes_service.find_all(col_meta_data, 'id', FilterTool({'$filter': {'id': 2}}))

        # this updates the index information, not the document itself
        self.indexes_service.update_indexes(col_meta_data, {'id': 2}, {'id': 20})

        new_lines = self.indexes_service.find_all(col_meta_data, 'id', FilterTool({'$filter': {'id': 20}}))

        self.assertEqual(len(new_lines), 1)
        self.assertListEqual(lines, new_lines)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(IndexesServiceTest) 
