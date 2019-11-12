import unittest
import os

from app.services.collections_service import CollectionsService
from app.tools.database_context import DatabaseContext

class CollectionsServiceTest(unittest.TestCase):

    def setUp(self):
        DatabaseContext.DATA_FOLDER = 'data-test/'
        self.collections_service = CollectionsService()

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

    def suit():
        return unittest.TestLoader().loadTestsFromTestCase(CollectionsServiceTest)
