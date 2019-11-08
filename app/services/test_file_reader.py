import unittest

from app.services.file_reader import FileReader
from app.tools.search_context import SearchContext
from app.tools.database_context import DatabaseContext

class FileReaderTest(unittest.TestCase):

    def setUp(self):
        DatabaseContext.DATA_FOLDER = 'data-test/'
        self.file_reader = FileReader()

    def test_find_doc_in_file(self):
        search_context = SearchContext({'filter': {'id': 3}})
        results = self.file_reader.find_in_file('data-test/data1.txt', search_context)
        self.assertEqual(len(results), 1)

    def test_find_doc_in_second_file(self):
        search_context = SearchContext({'filter': {'id': 12}})
        results = self.file_reader.find(search_context)
        self.assertEqual(len(results), 1)

    def test_append_and_remove_doc_in_file(self):
        DatabaseContext.MAX_DOC_PER_FILE = 10000
        self.file_reader.append({'id': 123})
        self.assertEqual(self.file_reader.file_len('data-test/data1.txt'), 4)

        self.file_reader.update(123, None)
        self.assertEqual(self.file_reader.file_len('data-test/data1.txt'), 3)

    def test_append_and_remove_doc_to_new_file(self):
        DatabaseContext.MAX_DOC_PER_FILE = 3
        self.file_reader.append({'id': 123})
        self.assertEqual(self.file_reader.file_len('data-test/data3.txt'), 1)

        self.file_reader.update(123, None)
        self.assertEqual(self.file_reader.file_len('data-test/data3.txt'), 0)

    def test_read_file_length(self):
        self.assertEqual(self.file_reader.file_len('data-test/data1.txt'), 3)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(FileReaderTest)
