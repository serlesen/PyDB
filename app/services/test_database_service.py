import unittest

from app.services.database_service import DatabaseService

class DatabaseServiceTest(unitttest.TestCase):

    @classmethod
    def setUpClass(cls):
        CollectionsSimulator.build_single_col('col')

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

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(DatabaseServiceTest)
