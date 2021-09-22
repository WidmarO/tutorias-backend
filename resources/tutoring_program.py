from flask_restful import Resource
from flask import request

from models.tutoring_program import TutoringProgramModel
from models.coordinator import CoordinatorModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt


class TutoringProgram(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_tutoring_program', str, True)
    parser.add_argument('title', str, True)
    parser.add_argument('initial_date', str, True)
    parser.add_argument('final_date', str, True)
    parser.add_argument('semester', str, True)
    parser.add_argument('condition', str, True)
    
    @jwt_required()
    def put(self, cod_tutoring_program):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Verify if all attributes are in request and are of correct type
        ans, data = TutoringProgram.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Create an instance of TutoringProgramModel with the data provided
        tutoring_program = TutoringProgramModel.find_by_cod_tutoring_program(cod_tutoring_program)
        if tutoring_program:
            tutoring_program.update_data(**data)
            tutoring_program.save_to_db()
            return tutoring_program.json(), 200
        return {'message': 'Tutoring Program not found.'}, 404

    @jwt_required()
    def get(self, cod_tutoring_program):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Find tutoring program by cod_tutoring_program
        tutoring_program = TutoringProgramModel.find_by_cod_tutoring_program(cod_tutoring_program)
        if tutoring_program:
            return tutoring_program.json(), 200
        return {'message': 'Tutoring Program not found.'}, 404
    
    @jwt_required()
    def delete(self, cod_tutoring_program):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401                
        # Find tutoring program by cod_tutoring_program
        tutoring_program = TutoringProgramModel.find_by_cod_tutoring_program(cod_tutoring_program)
        if tutoring_program:
            tutoring_program.delete_from_db()
            return tutoring_program.json(), 200
        return {'message': 'Tutoring Program not found.'}


class TutoringProgramList(Resource):
    parser = Req_Parser()
    parser.add_argument('title', str, True)
    parser.add_argument('initial_date', str, True)
    parser.add_argument('final_date', str, True)
    parser.add_argument('semester', str, True)
    parser.add_argument('condition', str, True)
    
    
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Return all tutoring programs in database
        sort_tutoring_programs = [ tutoring_program.json() for tutoring_program in TutoringProgramModel.find_all()]
        sort_tutoring_programs = sorted(sort_tutoring_programs, key=lambda x: x[list(sort_tutoring_programs[0].keys())[0]])        
        return sort_tutoring_programs, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        
        # Verify if all attributes are in request and are of correct type
        ans, data = TutoringProgramList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Get the coordinator
        email_coordinator = claims['sub']
        coordinator = CoordinatorModel.find_email_in_tutoring_program(email_coordinator)
        if not coordinator:
            return {'message': 'Coordinator not found'}, 404
        # Create a tutoring program 
        cod_tutoring_program = self.create_cod_tutoring_program()
        # Add or created a new tutoring program in database if already them not exist
        if TutoringProgramModel.find_by_cod_tutoring_program(cod_tutoring_program):
            return {'message': "A tutoring program with cod_tutoring_program: '{}' already exist".format(cod_tutoring_program)}
        
        # Add data for create the tutoring program
        data['cod_tutoring_program'] = cod_tutoring_program 
        data['cod_coordinator'] = coordinator.cod_coordinator        
        tutoring_program = TutoringProgramModel(**data)        
        try:
            tutoring_program.save_to_db()
        except:
            return {'message': "An error ocurred while create the tutoring program"}, 500
        return tutoring_program.json(), 201

    
    def create_cod_tutoring_program(self):
        list_tutoring_programs = TutoringProgramModel.find_all()
        list_tutoring_programs = [ tutoring_program.json() for tutoring_program in list_tutoring_programs]
        list_tutoring_programs = sorted(list_tutoring_programs, key=lambda x: x[list(list_tutoring_programs[0].keys())[0]])
        if len(list_tutoring_programs) == 0 :
            return 'PT-001'
        _max = list_tutoring_programs[-1]['cod_tutoring_program']
        _max = str(_max)
        entero=int(_max[-3:])
        new_code = _max[:3] + '{:>03}'.format(str(entero+1))
        return new_code