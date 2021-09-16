from flask_restful import Resource
from flask import request
from models.principal import PrincipalModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt


class Principal(Resource):
    parser = Req_Parser() 
    parser.add_argument('cod_principal', str, True)
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('cod_tutoring_program', str, True)

    @jwt_required()
    def put(self, cod_principal):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Verify if all arguments are correct
        ans, data = PrincipalList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if principal exists in database
        principal = PrincipalModel.find_by_cod_principal(cod_principal)
        if principal:
            principal.update_data(**data)
            principal.save_to_db()
            return principal.json(), 200

        return {'message': 'Director Principal not found.'}, 404

    def get(self, cod_principal):
        # Return a teacher if found in database
        principal = PrincipalModel.find_by_cod_principal(cod_principal)
        if principal:
            return teacher.json(), 200
        return {'message': 'Director Principal not found'}, 404

    @jwt_required()
    def delete(self, cod_principal):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Delete a teacher from database if exist in it
        principal = PrincipalModel.find_by_cod_principal(cod_principal)
        if principal:
            principal.delete_from_db()
            return principal.json(), 200

        # Return a messagge if not found
        return {'message': 'Director Principal not found.'}, 404


class PrincipalList(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_principal', str, True)
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('cod_tutoring_program', str, True)
    
    @jwt_required()
    def get(self):
        claims = get_jwt()

        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all teachers in database        
        sort_principal = [ principal.json() for principal in PrincipalModel.find_all() ]
        sort_principal = sorted(sort_principal, key=lambda x: x[list(sort_principal[0].keys())[0]])
        
        return sort_principal, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()

        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Verify if all attributes are in request and are of corrects type
        ans, data = PrincipalList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if teacher already exists in database
        cod_principal = data['cod_principal']        
        if PrincipalModel.find_by_cod_principal(cod_principal):
            return {'message': "A principal director with cod_principal: '{}' already exist".format(cod_principal)}

        # Create a instance of TeacherModel with the data provided
        principal = PrincipalModel(**data)

        # Try to insert the teacher in database
        try:
            principal.save_to_db()
        except:
            return {'message': "An error ocurred when adding the principal in DB"}, 500

        # Return the teacher data with a status code 201
        return principal.json(), 201

