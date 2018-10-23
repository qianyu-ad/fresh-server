from flask import Blueprint
from flask_restful import Api
from fresh.api.base.urls import register_restful_api

bp = Blueprint('api', __name__)
api = Api(bp)

register_restful_api(api)