from flask import Blueprint

api_blueprint = Blueprint(name='api', url_prefix='/api', import_name=__name__)

from .views import * 
