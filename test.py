import unittest

from app.auth.test_permissions import PermissionsTest
from app.auth.test_roles import RolesTest
from app.controllers.test_auth_controller import AuthControllerTest
from app.controllers.test_bulk_controller import BulkControllerTest
from app.controllers.test_collections_controller import CollectionsControllerTest
from app.controllers.test_crud_controller import CrudControllerTest
from app.controllers.test_database_controller import DatabaseControllerTest
from app.controllers.test_replication_controller import ReplicationControllerTest
from app.controllers.test_search_controller import SearchControllerTest
from app.services.test_auth_service import AuthServiceTest
from app.services.test_collections_service import CollectionsServiceTest
from app.services.test_crud_service import CrudServiceTest
from app.services.test_database_service import DatabaseServiceTest
from app.services.test_data_service import DataServiceTest
from app.services.test_files_reader import FilesReaderTest
from app.services.test_indexes_service import IndexesServiceTest
from app.services.test_search_service import SearchServiceTest
from app.threads.test_cleaning_thread import CleaningThreadTest
from app.threads.test_replication_thread import ReplicationThreadTest
from app.tools.test_filter_tool import FilterToolTest
from app.tools.test_collection_meta_data import CollectionMetaDataTest
from app.tools.test_results_mapper import ResultsMapperTest
from app.tools.test_search_context import SearchContextTest

def suite():
    return unittest.TestSuite([
        AuthControllerTest.suite(),
        AuthServiceTest.suite(),
        BulkControllerTest.suite(),
        CleaningThreadTest.suite(),
        CollectionMetaDataTest.suite(),
        CollectionsControllerTest.suite(),
        CollectionsServiceTest.suite(),
        CrudControllerTest.suite(),
        CrudServiceTest.suite(),
        DatabaseControllerTest.suite(),
        DatabaseServiceTest.suite(),
        DataServiceTest.suite(),
        FilesReaderTest.suite(),
        FilterToolTest.suite(),
        IndexesServiceTest.suite(),
        PermissionsTest.suite(),
        ReplicationControllerTest.suite(),
        ReplicationThreadTest.suite(),
        ResultsMapperTest.suite(),
        RolesTest.suite(),
        SearchContextTest.suite(),
        SearchControllerTest.suite(),
        SearchServiceTest.suite()
        ])

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
