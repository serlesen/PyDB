import unittest
import os
import _pickle as pickle

from app.services.file_reader import FileReader
from app.test.collections_simulator import CollectionsSimulator
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext
from app.tools.filter_tool import FilterTool

class FileReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col')

    def setUp(self):
        # instanciate the service to test
        self.file_reader = FileReader()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def test_find_one_doc_in_file(self):
        filter_tool = FilterTool({'$filter': {'id': 3}})
        result = self.file_reader.find_one_in_file('data-test/col/data1.bin', filter_tool)
        self.assertEqual(result['id'], 3)

    def test_append_doc_in_file(self):
        DatabaseContext.MAX_DOC_PER_FILE = 10000
        self.file_reader.append(CollectionMetaData('col'), {'id': 123})
        self.assertEqual(self.file_reader.file_len('data-test/col/data2.bin'), 4)

    def test_append_doc_to_new_file(self):
        DatabaseContext.MAX_DOC_PER_FILE = 3
        col_meta_data = CollectionMetaData('col')
        self.file_reader.append(col_meta_data, {'id': 123})
        self.assertEqual(self.file_reader.file_len('data-test/col/data3.bin'), 1)

        col_meta_data.remove_last_data_file()

    def test_remove_doc_in_file(self):
        result = self.file_reader.update(CollectionMetaData('col'), 6, {})
        self.assertEqual(result, {})

        filter_tool = FilterTool({'$filter': {'id': 6}})
        result = self.file_reader.find_one_in_file('data-test/col/data2.bin', filter_tool)
        self.assertIsNone(result)

    def test_read_file_length(self):
        self.assertEqual(self.file_reader.file_len('data-test/col/data1.bin'), 3)

    def test_update_value(self):
        self.file_reader.update(CollectionMetaData('col'), 2, {'id': 2, 'first_name': 'Joooooohn', 'last_name': 'Smith'})
        self.assertEqual(self.file_reader.file_len('data-test/col/data1.bin'), 3)

        filter_tool = FilterTool({'$filter': {'first_name': 'Joooooohn'}})
        result = self.file_reader.find_one_in_file('data-test/col/data1.bin', filter_tool)
        self.assertEqual(result['id'], 2)
        self.assertEqual(result['first_name'], 'Joooooohn')

        self.file_reader.update(CollectionMetaData('col'), 2, {'id': 2, 'first_name': 'John', 'last_name': 'Smith'})
        results = self.file_reader.find_one_in_file('data-test/col/data1.bin', filter_tool)
        self.assertIsNone(results)


    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(FileReaderTest)

