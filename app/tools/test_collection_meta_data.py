import unittest

from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CollectionMetaDataTest(unittest.TestCase):

    def setUp(self):
        DatabaseContext.DATA_FOLDER = 'data-test/'

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

        result = meta_data.add_index('id')
        self.assertEqual(result['status'], 'done')
        self.assertEqual(meta_data.indexes['id'], 'id.idx')

        meta_data.remove_index('id')
        self.assertEqual(result['status'], 'done')
        self.assertTrue('id' not in meta_data.indexes)

    def suite():
        return unittest.TestLoader.loadTestsFromTestCase(CollectionMetaDataTest)
