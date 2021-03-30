from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.aplication import AplicationModel
from Req_Parser import Req_Parser


class AplicationList(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('aplication', str, True)
    # @jwt_required()

    def get(self):
        sort_aplications = list(
            map(lambda x: x.json(), AplicationModel.query.all()))
        sort_aplications = sorted(
            sort_aplications, key=lambda x: x[list(sort_aplications[0].keys())[0]])
        print(sort_aplications)
        return sort_aplications

    def post(self):

        print(request.json)
        aplication = request.json['aplication']
        '''Add or created a new aplication in database if already them not exist'''
        if AplicationModel.find_by_aplication(aplication):
            return {'message': "A aplication: '{}' already exist in data base".format(aplication)}

        ans, data = AplicationList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        aplication = AplicationModel(**data)

        try:
            aplication.save_to_db()
        except:
            return {'message': "An error ocurred adding the aplication"}, 500

        return aplication.json(), 201

    def delete(self):
        '''Delete a aplication from database if exist in it'''
        print(request.json)
        aplication = request.json['aplication']
        aplication = AplicationModel.find_by_aplication(aplication)
        if aplication:
            aplication.delete_from_db()
            return aplication.json(), 200

        return {'message': 'Aplication not found.'}
