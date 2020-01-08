import unittest
import os
import _pickle as pickle

from app.services.data_service import DataService
from app.test.collections_simulator import CollectionsSimulator
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext
from app.tools.filter_tool import FilterTool

class DataServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col', None)

    def setUp(self):
        # instanciate the service to test
        self.data_service = DataService()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def test_find_by_line_first_file_actual_thread(self):
        docs = self.data_service.find_by_line(CollectionMetaData('col'), [1], 1)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['id'], 2)

    def test_find_by_line_first_file_next_thread(self):
        docs = self.data_service.find_by_line(CollectionMetaData('col'), [1], 2)
        self.assertEqual(len(docs), 0)

    def test_find_by_line_second_file_previous_thread(self):
        docs = self.data_service.find_by_line(CollectionMetaData('col'), [4], 1)
        self.assertEqual(len(docs), 0)

    def test_find_by_line_second_file_actual_thread(self):
        docs = self.data_service.find_by_line(CollectionMetaData('col'), [4], 2)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['id'], 5)

    def test_find_by_multiple_lines_but_found_first_one(self):
        docs = self.data_service.find_by_line(CollectionMetaData('col'), [1, 4], 1)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['id'], 2)

    def test_find_by_multiple_lines_but_found_second_one(self):
        docs = self.data_service.find_by_line(CollectionMetaData('col'), [1, 4], 2)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['id'], 5)

    def test_find_one_doc_in_file(self):
        filter_tool = FilterTool({'$filter': {'id': 3}})
        result = self.data_service.find_one_in_file('data-test/col/data1.bin', filter_tool)
        self.assertEqual(result['id'], 3)

    def test_append_doc_in_file(self):
        DatabaseContext.MAX_DOC_PER_FILE = 10000
        self.data_service.append(CollectionMetaData('col'), [{'id': 123}])
        self.assertEqual(self.data_service.file_len('data-test/col/data2.bin'), 4)

    def test_append_doc_to_new_file(self):
        DatabaseContext.MAX_DOC_PER_FILE = 3
        col_meta_data = CollectionMetaData('col')
        self.data_service.append(col_meta_data, [{'id': 123}])
        self.assertEqual(self.data_service.file_len('data-test/col/data3.bin'), 1)

        col_meta_data.remove_last_data_file()

    def test_append_bulk(self):
        DatabaseContext.MAX_DOC_PER_FILE = 3
        col_meta_data = CollectionMetaData('col')
        self.data_service.append(col_meta_data, [{'id': 201}, {'id': 202}, {'id': 203}, {'id': 204}, {'id': 205}])
        self.assertEqual(self.data_service.file_len('data-test/col/data3.bin'), 3)
        self.assertEqual(self.data_service.file_len('data-test/col/data4.bin'), 2)

        col_meta_data.remove_last_data_file()
        col_meta_data.remove_last_data_file()

    def test_remove_doc_in_file(self):
        result = self.data_service.update(CollectionMetaData('col'), [6], [{}])[0]
        self.assertEqual(result, {'line': 2, 'doc': {}})

        filter_tool = FilterTool({'$filter': {'id': 6}})
        result = self.data_service.find_one_in_file('data-test/col/data2.bin', filter_tool)
        self.assertIsNone(result)

    def test_read_file_length(self):
        self.assertEqual(self.data_service.file_len('data-test/col/data1.bin'), 3)

    def test_update_value(self):
        self.data_service.update(CollectionMetaData('col'), [2], [{'id': 2, 'first_name': 'Joooooohn', 'last_name': 'Smith'}])
        self.assertEqual(self.data_service.file_len('data-test/col/data1.bin'), 3)

        filter_tool = FilterTool({'$filter': {'first_name': 'Joooooohn'}})
        result = self.data_service.find_one_in_file('data-test/col/data1.bin', filter_tool)
        self.assertEqual(result['id'], 2)
        self.assertEqual(result['first_name'], 'Joooooohn')

        self.data_service.update(CollectionMetaData('col'), [2], [{'id': 2, 'first_name': 'John', 'last_name': 'Smith'}])
        results = self.data_service.find_one_in_file('data-test/col/data1.bin', filter_tool)
        self.assertIsNone(results)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(DataServiceTest)

