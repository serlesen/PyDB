from flask import Flask

from app.injection.dependency_injections_service import DependencyInjectionsService
from app.services.collections_service import CollectionsService
from app.services.crud_service import CrudService
from app.services.database_service import DatabaseService
from app.services.file_reader import FileReader
from app.services.indexes_service import IndexesService
from app.services.query_manager import QueryManager
from app.services.search_service import SearchService
from app.threads.threads_manager import ThreadsManager

app = Flask(__name__)

collections_service = DependencyInjectionsService.get_instance().get_service(CollectionsService)
crud_service = DependencyInjectionsService.get_instance().get_service(CrudService)
database_service = DependencyInjectionsService.get_instance().get_service(DatabaseService)
file_reader = DependencyInjectionsService.get_instance().get_service(FileReader)
indexes_service = DependencyInjectionsService.get_instance().get_service(IndexesService)
query_manager = DependencyInjectionsService.get_instance().get_service(QueryManager)
search_service = DependencyInjectionsService.get_instance().get_service(SearchService)

ThreadsManager().start()

from app.controllers import bulk_controller
from app.controllers import collections_controller
from app.controllers import crud_controller
from app.controllers import database_controller
from app.controllers import errors_controller
from app.controllers import search_controller
