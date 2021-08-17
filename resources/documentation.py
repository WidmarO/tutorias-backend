from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.brand import BrandModel
from Req_Parser import Req_Parser


class BrandList(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('brand', str, True)
    # @jwt_required()

    def get(self):
        return "<h1>Documentacion<h1>"