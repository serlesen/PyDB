import unittest
import os
import _pickle as pickle

from app.test.collections_simulator import CollectionsSimulator
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CollectionMetaDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col')

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def test_read_counter(self):
        meta_data = CollectionMetaData('col')
        self.assertEqual(meta_data.counter, 2)

    def test_last_data_file(self):
        meta_data = CollectionMetaData('col')
        self.assertEqual(meta_data.last_data_fname(), 'data2.bin')

    def test_enumerate_file_names(self):
        meta_data = CollectionMetaData('col')
        self.assertListEqual(meta_data.enumerate_data_fnames(), ['data1.bin', 'data2.bin'])

    def test_add_remove_index(self):
        meta_data = CollectionMetaData('col')

        result = meta_data.add_or_update_index('id', 10)
        self.assertEqual(result['status'], 'done')
        self.assertEqual(meta_data.indexes['id'], 10)

        meta_data.remove_index('id')
        self.assertEqual(result['status'], 'done')
        self.assertTrue('id' not in meta_data.indexes)

    def suite():
        return unittest.TestLoader.loadTestsFromTestCase(CollectionMetaDataTest)
