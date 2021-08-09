from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.part_number import PartNumberModel
from Req_Parser import Req_Parser


class PartNumber(Resource):

    def get(self, id):
        # get the value if exist
        part = PartNumberModel.find_by_id(id)
        if part:
            print("si se encontro en part_number", part)
            return part.json()
        return {'message': "part_number with id '{}'not found".format(id)}, 404


class PartNumberList(Resource):
    parser = Req_Parser()
    parser.add_argument('part_number', str, True)
    # @jwt_required()

    def get(self):
        sort_part_numbers = list(
            map(lambda x: x.json(), PartNumberModel.query.all()))
        sort_part_numbers = sorted(
            sort_part_numbers, key=lambda x: x[list(sort_part_numbers[0].keys())[0]])
        print(sort_part_numbers)
        return sort_part_numbers

    def add_part(part_number):
        # get the new id value
        _list = list(map(lambda x: x.json(), PartNumberModel.query.all()))
        new_id = 0
        for i in _list:
            if i['id'] > new_id:
                new_id = i['id']
        id = new_id + 1
        part_number = PartNumberModel(id, part_number)

        try:
            part_number.save_to_db()
        except:
            return False, {'message': "An error ocurred adding the part_number"}

        return True, part_number.json(), 201

    def post(self):

        print(request.json)
        part_number = request.json['part_number']

        '''Add or created a new part_number in database if already them not exist'''
        if PartNumberModel.find_by_part_number(part_number):
            return {'message': "A part_number: '{}' already exist in data base".format(part_number)}

            # get the new id value
        _list = list(map(lambda x: x.json(), PartNumberModel.query.all()))
        new_id = 0
        for i in _list:
            if i['id'] > new_id:
                new_id = i['id']
        id = new_id + 1

        ans, data = PartNumberList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        part_number = PartNumberModel(id, **data)

        try:
            part_number.save_to_db()
        except:
            return {'message': "An error ocurred adding the part_number"}, 500

        return part_number.json(), 201

    def delete(self):
        '''Delete a part_number from database if exist in it'''
        print(request.json)
        part_number = request.json['part_number']
        part_number = PartNumberModel.find_by_part_number(part_number)
        if part_number:
            part_number.delete_from_db()
            return part_number.json(), 200

        return {'message': 'part_number not found.'}
