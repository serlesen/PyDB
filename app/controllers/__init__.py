from flask import Flask
from app.services.search_service import SearchService
from app.services.crud_service import CrudService

app = Flask(__name__)

search_service = SearchService()
crud_service = CrudService()

from app.controllers import bulk_controller
from app.controllers import crud_controller
from app.controllers import errors_controller
from app.controllers import search_controller
