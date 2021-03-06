import unittest

from app.services.database_service import DatabaseService
from app.test.collections_simulator import CollectionsSimulator

class DatabaseServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col', None)

    def setUp(self):
        # instanciate the service to test
        self.database_service = DatabaseService()

    @classmethod
    def tearDownClass(cls):
        CollectionsSimulator.clean()

    def test_database_service(self):
        status = self.database_service.get_status()

        self.assertTrue('collections' in status)
        self.assertEqual(len(status['collections']), 1)
        self.assertEqual(status['collections'][0]['collection'], 'col')

        self.assertTrue('cleaning_operations' in status)
        self.assertEqual(len(status['cleaning_operations']), 0)

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(DatabaseServiceTest)
