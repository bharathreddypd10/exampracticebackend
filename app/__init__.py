from flask import Blueprint
from flask_restx import Api
from app.app_main.controllers.users import (signup_blueprint)

blueprint= Blueprint('api',__name__)
api=Api(blueprint,title="Vehicle Service")
api.add_namespace(signup_blueprint)
