from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.new import NewModel
from Req_Parser import Req_Parser


class Student(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_new', str, True)
    parser.add_argument('title', str, True)
    parser.add_argument('description', str, True)
    parser.add_argument('whom', str, True)
    parser.add_argument('date_time', str, True)
    parser.add_argument('cod_tutoring_program', str, True)

    def put(self, cod_new):
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

    # @jwt_required()
    def delete(self, cod_new):

        # Delete a student from database if exist in it
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
    
    # @jwt_required()
    def get(self):
        # Return all news in database        
        sort_news = [ new.json() for new in NewModel.find_all() ]
        sort_news = sorted(sort_news, key=lambda x: x[list(sort_news[0].keys())[0]])
        print(sort_news)
        return sort_news, 200


    def post(self):

        # Verify if all attributes are in request and are of corrects type
        ans, data = NewList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if new already exists in database
        cod_new = data['cod_new']        
        if NewModel.find_by_cod_new(cod_new):
            return {'message': "A new with cod_new: '{}' already exist".format(cod_new)}

        # Create a instance of NewModel with the data provided
        new = NewModel(**data)

        # Try to insert the new in database
        try:
            new.save_to_db()
        except:
            return {'message': "An error ocurred when adding the new in DB"}, 500

        # Return the new data with a status code 201
        return new.json(), 201