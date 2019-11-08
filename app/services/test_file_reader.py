import unittest
from app.services.file_reader import FileReader
from app.tools.search_context import SearchContext

class FileReaderTest(unittest.TestCase):

    def setUp(self):
        self.file_reader = FileReader()

    def test_file_doc_in_file(self):
        search_context = SearchContext({'filter': {'id': 3}})

        results = self.file_reader.find_in_file('src/unittest/resources/data1.txt', search_context)

        self.assertEqual(len(results), 1)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(FileReaderTest)
