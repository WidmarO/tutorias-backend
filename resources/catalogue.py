from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.catalogue import CatalogueModel
from Req_Parser import Req_Parser
import functools


class Catalogue(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('model', str, required=True)
    parser.add_argument('brand', str, required=True)
    parser.add_argument('part_number', str, required=True)
    parser.add_argument('motor', str, required=True)
    parser.add_argument('aplication', str, required=True)

    # @jwt_required()
    def get(self, id):
        '''Search client by name in the database and return it if is founded'''
        catalogue = CatalogueModel.find_by_id(id)
        if catalogue:
            return catalogue.json()
        return {'message': 'catalogue not found'}, 404

    def put(self, id):

        ans, data = CatalogueList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        catalogue = CatalogueModel.find_by_id(id)

        if catalogue:
            catalogue.update_data(**data)
        else:
            return {'message': "catalogue not found."}

        catalogue.save_to_db()
        catalogue_list = CatalogueList()
        return catalogue_list.get()

    def delete(self, id):
        '''Delete a catalogue index from database if exist in it'''
        catalogue = CatalogueModel.find_by_id(id)
        if catalogue:
            catalogue.delete_from_db()
            return catalogue.json(), 200

        return {'message': 'Client not found.'}


class CatalogueList(Resource):
    parser = Req_Parser()
    parser.add_argument('id', int, esp_attr=True)
    parser.add_argument('model', str, required=True)
    parser.add_argument('brand', str, required=True)
    parser.add_argument('part_number', str, required=True)
    parser.add_argument('motor', str, required=True)
    parser.add_argument('aplication', str, required=True)

    # @jwt_required()
    def get(self):
        sort_catalogue = list(
            map(lambda x: x.json(), CatalogueModel.query.all()))
        sort_catalogue = sorted(
            sort_catalogue, key=lambda x: x[list(sort_catalogue[0].keys())[0]])
        print(sort_catalogue)
        return sort_catalogue

    def post(self):
        _list = list(map(lambda x: x.json(), CatalogueModel.query.all()))
        new_id = 0        
        for i in _list:
            if i['id'] > new_id:
                new_id = i['id']

        id = new_id + 1
        
        model = request.json['model']
        brand = request.json['brand']
        part_number = request.json['part_number']
        motor = request.json['motor']
        aplication = request.json['aplication']
        '''Add or created a new brand in database if already them0 not exist'''
        if CatalogueModel.find_by_id(id):
            return {'message': "A catalogue: '{}' already exist in data base".format(id)}

        ans, data = CatalogueList.parser.parse_args(dict(request.json))
        print(data)
        if not ans:
            return data

        catalogue = CatalogueModel(id, **data)

        try:
            catalogue.save_to_db()
        except:
            return {'message': "An error ocurred adding the combination for catalogue"}, 500

        return catalogue.json(), 201
