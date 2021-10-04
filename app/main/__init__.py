from flask import Blueprint

main_blueprint = Blueprint(name='main', url_prefix='/', import_name=__name__)
from .views import * 