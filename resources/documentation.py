from flask_restful import Resource
from flask import request, render_template, make_response
from Req_Parser import Req_Parser


class Documentation(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('brand', str, True)
    # @jwt_required()

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation.html'),200,headers)

