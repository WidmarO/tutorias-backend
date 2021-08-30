from datetime import datetime
from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.tutoring_program import TutoringProgramModel
from Req_Parser import Req_Parser

class TutoringProgram(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_tutoring_program', str, True)
    parser.add_argument('title', str, True)
    parser.add_argument('inicial_date', datetime, True)
    parser.add_argument('final_date', datetime, True)
    parser.add_argument('semester', str, True)
    parser.add_argument('condition', bool, True)
    parser.add_argument('cod_coordinator', str, True)
    # @jwt_required()

    def put(self, cod_tutoring_program):
        # Verify if all attributes are in request and are of correct type
        ans, data = TutoringProgramList.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # Create a instance of TutoringProgramModel with the data provided
        tutoring_program = TutoringProgramModel.find_by_cod_tutoring_program(cod_tutoring_program)
        if tutoring_program:
            tutoring_program.update_data(**data)
            tutoring_program.save_to_db()
            return tutoring_program.json(), 200
        return {'message': 'Tutoring Program not found.'}, 404

    def get(self, cod_tutoring_program):
        tutoring_program = TutoringProgramModel.find_by_cod_tutoring_program(cod_tutoring_program)
        if tutoring_program:
            return tutoring_program.json(), 200
        return {'message': 'Tutoring Program not found.'}, 404
    
    def delete(self, cod_tutoring_program):
        '''Delete a tutoring program from database if exist in it'''
        #print(request.json)
        #cod_tutoring_program = request.json['cod_tutoring_program']

        tutoring_program = TutoringProgramModel.find_by_cod_tutoring_program(cod_tutoring_program)
        if tutoring_program:
            tutoring_program.delete_from_db()
            return tutoring_program.json(), 200

        return {'message': 'Tutoring Program not found.'}


class TutoringProgramList(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_tutoring_program', str, True)
    parser.add_argument('title', str, True)
    parser.add_argument('inicial_date', datetime, True)
    parser.add_argument('final_date', datetime, True)
    parser.add_argument('semester', str, True)
    parser.add_argument('condition', bool, True)
    parser.add_argument('cod_coordinator', str, True)
    # @jwt_required()

    def get(self):

        # Return all tutoring programs in database
        sort_tutoring_programs = [ tutoring_program.json() for tutoring_program in TutoringProgramModel.find_all()]
        sort_tutoring_programs = sorted(sort_tutoring_programs, key=lambda x: x[list(sort_tutoring_programs[0].keys())[0]])
        print(sort_tutoring_programs)
        return sort_tutoring_programs
        # return {'message': 'List of Tutoring Program'}


    def post(self):

        print(request.json)
        cod_tutoring_program = request.json['cod_tutoring_program']
        '''Add or created a new tutoring program in database if already them not exist'''
        if TutoringProgramModel.find_by_cod_tutoring_program(cod_tutoring_program):
            return {'message': "A tutoring program with cod_tutoring_program: '{}' already exist".format(cod_tutoring_program)}
        # Verify if all attributes are in request and are of correct type
        ans, data = TutoringProgramList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Create a instance of TutoringProgramModel with the data provided
        tutoring_program = TutoringProgramModel(**data)

        try:
            tutoring_program.save_to_db()
        except:
            return {'message': "An error ocurred adding the tutoring program"}, 500

        return tutoring_program.json(), 201
