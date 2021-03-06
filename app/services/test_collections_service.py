import unittest
import os

from app.services.collections_service import CollectionsService
from app.test.collections_simulator import CollectionsSimulator
from app.tools.collection_meta_data import CollectionMetaData
from app.tools.database_context import DatabaseContext

class CollectionsServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col', None)

    def setUp(self):
        # instanciate the service to test
        self.collections_service = CollectionsService()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def test_create_collection(self):
        result = self.collections_service.create('new_col')
        self.assertEqual(result['status'], 'done')
        self.assertTrue(os.path.exists(DatabaseContext.DATA_FOLDER + 'new_col'))

        result = self.collections_service.remove('new_col')
        self.assertEqual(result['status'], 'done')
        self.assertFalse(os.path.exists(DatabaseContext.DATA_FOLDER + 'new_col'))

    def test_already_existing_collection(self):
        self.assertTrue(os.path.exists(DatabaseContext.DATA_FOLDER + 'col'))

        result = self.collections_service.create('col')
        self.assertEqual(result['status'], 'already existing')
        self.assertTrue(os.path.exists(DatabaseContext.DATA_FOLDER + 'col'))

    def test_missing_collection_to_remove(self):
        self.assertFalse(os.path.exists(DatabaseContext.DATA_FOLDER + 'new_col'))

        result = self.collections_service.remove('new_col')
        self.assertEqual(result['status'], 'missing collection')

    def test_get_status(self):
        status = self.collections_service.get_status('col')
        self.assertEqual(status['count'], 6)
        self.assertTrue('indexes' in status)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(CollectionsServiceTest)
