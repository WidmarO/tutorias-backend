from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.workshop import WorkshopModel
from Req_Parser import Req_Parser

class Workshop(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_workshop', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('cod_student_helper', str, True)
    parser.add_argument('classroom')
    parser.add_argument('schedule')
    parser.add_argument('cod_tutoring_program', str, True)
    # @jwt_required()

    def put(self, cod_workshop):
        # Verify if all attributes are in request and are of correct type
        ans, data = WorkshopList.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # Create a instance of WorkshopModel with the data provided
        workshop = WorkshopModel.find_by_cod_workshop(cod_workshop)
        if workshop:
            workshop.update_data(**data)
            workshop.save_to_db()
            return workshop.json(), 200
        return {'message': 'Workshop not found.'}, 404

    def get(self, cod_workshop):
        workshop = WorkshopModel.find_by_cod_workshop(cod_workshop)
        if workshop:
            return workshop.json(), 200
        return {'message': 'Workshop not found.'}, 404
    
    def delete(self, cod_workshop):
        '''Delete a workshop from database if exist in it'''
        #print(request.json)
        #cod_workshop = request.json['cod_workshop']

        workshop = WorkshopModel.find_by_cod_workshop(cod_workshop)
        if workshop:
            workshop.delete_from_db()
            return workshop.json(), 200

        return {'message': 'Workshop not found.'}


class WorkshopList(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_workshop', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('cod_student_helper', str, True)
    parser.add_argument('classroom', str)
    parser.add_argument('schedule', str)
    parser.add_argument('cod_tutoring_program', str, True)
    # @jwt_required()

    def get(self):

        # Return all workshops in database
        #sort_students = list(map(lambda x: x.json(), StudentModel.query.all()))
        sort_workshops = [ workshop.json() for workshop in WorkshopModel.find_all()]
        sort_workshops = sorted(sort_workshops, key=lambda x: x[list(sort_workshops[0].keys())[0]])
        print(sort_workshops)
        return sort_workshops
        # return {'message': 'List of workshops'}


    def post(self):

        print(request.json)
        cod_workshop = request.json['cod_workshop']
        '''Add or created a new student in database if already them not exist'''
        if WorkshopModel.find_by_cod_workshop(cod_workshop):
            return {'message': "A workshop with cod_workshop: '{}' already exist".format(cod_workshop)}
        # Verify if all attributes are in request and are of correct type
        ans, data = WorkshopList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Create a instance of WorkshopModel with the data provided
        workshop = WorkshopModel(**data)

        try:
            workshop.save_to_db()
        except:
            return {'message': "An error ocurred adding the workshop"}, 500

        return workshop.json(), 201
