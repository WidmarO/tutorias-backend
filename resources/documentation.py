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

class Documentation_coordinator(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('brand', str, True)
    # @jwt_required()

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation_coordinator.html'),200,headers)

class Documentation_principal(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('brand', str, True)
    # @jwt_required()

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation_principal.html'),200,headers)

class Documentation_teacher(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('brand', str, True)
    # @jwt_required()

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation_teacher.html'),200,headers)        

class Documentation_student(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('brand', str, True)
    # @jwt_required()

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation_student.html'),200,headers)

class Documentation_tutor(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('brand', str, True)
    # @jwt_required()

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('documentation_tutor.html'),200,headers)  