from flask_restful import Resource
from flask import request
# from flask_jwt import jwt_required
from models.coordinator import CoordinatorModel
from Req_Parser import Req_Parser

class Coordinator(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_coordinator', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    # @jwt_required()

    def put(self, cod_coordinator):
        # Verify if all attributes are in request and are of correct type
        ans, data = CoordinatorList.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # Create a instance of CoordinatorModel with the data provided
        coordinator = CoordinatorModel.find_by_cod_coordinator(cod_coordinator)
        if coordinator:
            coordinator.update_data(**data)
            coordinator.save_to_db()
            return coordinator.json(), 200
        return {'message': 'Coordinator not found.'}, 404

    def get(self, cod_coordinator):
        coordinator = CoordinatorModel.find_by_cod_coordinator(cod_coordinator)
        if coordinator:
            return coordinator.json(), 200
        return {'message': 'Coordinator not found.'}, 404

    def delete(self, cod_coordinator):
        '''Delete a coodinator from database if exist in it'''
        coordinator = CoordinatorModel.find_by_cod_coordinator(cod_coordinator)
        if coordinator:
            coordinator.delete_from_db()
            return coordinator.json(), 200

        return {'message': 'Coordinator not found.'}


class CoordinatorList(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_coordinator', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    # @jwt_required()

    def get(self):
        sort_coordinators = [ coordinator.json() for coordinator in CoordinatorModel.find_all()]
        sort_coordinators = sorted(sort_coordinators, key=lambda x: x[list(sort_coordinators[0].keys())[0]])
        print(sort_coordinators)
        return sort_coordinators
        # return {'message': 'List of coordinator'}


    def post(self):
        print(request.json)
        cod_coordinator = request.json['cod_coordinator']
        '''Add or created a new coordinator in database if already them not exist'''
        if CoordinatorModel.find_by_cod_coordinator(cod_coordinator):
            return {'message': "A coordinator with cod_coordinator: '{}' already exist".format(cod_coordinator)}

        ans, data = CoordinatorList.parser.parse_args(dict(request.json))

        if not ans:
            return data

        coordinator = CoordinatorModel(**data)

        try:
            coordinator.save_to_db()
        except:
            return {'message': "An error ocurred adding the coordinator"}, 500

        return coordinator.json(), 201