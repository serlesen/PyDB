from flask import Flask
from app.services.collections_service import CollectionsService
from app.services.crud_service import CrudService
from app.services.database_service import DatabaseService
from app.services.search_service import SearchService

app = Flask(__name__)

collections_service = CollectionsService()
crud_service = CrudService()
database_service = DatabaseService()
search_service = SearchService()

from app.controllers import bulk_controller
from app.controllers import collections_controller
from app.controllers import crud_controller
from app.controllers import database_controller
from app.controllers import errors_controller
from app.controllers import search_controller
