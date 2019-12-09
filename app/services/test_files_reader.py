import unittest

from app.services.files_reader import FilesReader
from app.test.collections_simulator import CollectionsSimulator
from app.tools.database_context import DatabaseContext


class FilesReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_big_col('col')

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()
        DatabaseContext.CACHE_FILE_SIZE = 100

    def test_read_file_from_cache(self):
        FilesReader.get_instance().reset()

        self.assertFalse('data-test/col/data1.bin' in FilesReader.get_instance().files)

        FilesReader.get_instance().get_file_content('data-test/col/data1.bin')

        self.assertTrue('data-test/col/data1.bin' in FilesReader.get_instance().files)

    def test_clean_oldest_data(self):
        DatabaseContext.CACHE_FILE_SIZE = 1 # each data file is about 800kb
        FilesReader.get_instance().reset()

        FilesReader.get_instance().get_file_content('data-test/col/data1.bin')
        FilesReader.get_instance().get_file_content('data-test/col/data2.bin')

        self.assertFalse('data-test/col/data1.bin' in FilesReader.get_instance().files)
        self.assertTrue('data-test/col/data2.bin' in FilesReader.get_instance().files)

    
    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(FilesReaderTest)
