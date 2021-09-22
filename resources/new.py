from flask_restful import Resource
from flask import request
from models.new import NewModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt


class New(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_new', str, True)
    parser.add_argument('title', str, True)
    parser.add_argument('description', str, True)
    parser.add_argument('whom', str, True)
    parser.add_argument('date_time', str, True)
    parser.add_argument('cod_tutoring_program', str, True)

    @jwt_required()
    def put(self, cod_new):
        claims = get_jwt()

        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Verify if all arguments are correct
        ans, data = NewList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if new exists in database
        new = NewModel.find_by_cod_new(cod_new)
        if new:
            new.update_data(**data)
            new.save_to_db()
            return new.json(), 200

        return {'message': 'New not found.'}, 404

    def get(self, cod_new):
        # Return a new if found in database
        new = NewModel.find_by_cod_new(cod_new)
        if new:
            return new.json(), 200
        return {'message': 'New not found'}, 404

    def delete(self, cod_new):
        '''Delete a new from database if exist in it'''
        new = NewModel.find_by_cod_new(cod_new)
        if new:
            new.delete_from_db()
            return new.json(), 200

        # Return a messagge if not found
        return {'message': 'New not found.'}, 404


class NewList(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_new', str, True)
    parser.add_argument('title', str, True)
    parser.add_argument('description', str, True)
    parser.add_argument('whom', str, True)
    parser.add_argument('date_time', str, True)
    parser.add_argument('cod_tutoring_program', str, True)  
    
    def get(self):
        
        # Return all news in database        
        sort_news = [ new.json() for new in NewModel.find_all() ]
        sort_news = sorted(sort_news, key=lambda x: x[list(sort_news[0].keys())[0]])
        print(sort_news)
        return sort_news, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        print(request.json)
        cod_new = request.json['cod_new']
        '''Add or created a new 'new' in database if already them not exist'''
        if NewModel.find_by_cod_new(cod_new):
            return {'message': "A new with cod_new: '{}' already exist".format(cod_new)}
        # Verify if all attributes are in request and are of correct type
        ans, data = NewList.parser.parse_args(dict(request.json))
        if not ans:
            return data 
        # Create a instance of NewModel with the data provided
        new = NewModel(**data)

        try:
            new.save_to_db()
        except:
            return {'message': "An error ocurred adding the new"}, 500

        return new.json(), 201


class NewListTutoringProgram(Resource):
    
    @jwt_required()
    def get(self, cod_tutoring_program):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all students in database        
        list_new_in_tutoring_program = [ new.json() for new in NewModel.find_by_cod_tutoring_program(cod_tutoring_program) ]
        list_new_in_tutoring_program = sorted(list_new_in_tutoring_program, key=lambda x: x[list(list_new_in_tutoring_program[0].keys())[0]])    
        return list_new_in_tutoring_program, 200
