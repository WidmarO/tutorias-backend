from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from Req_Parser import Req_Parser

# Importing the models and other resources requireds
from resources.part_numbers import PartNumberList
from models.part_number import PartNumberModel
from models.part_aplication import PartAplicationModel
from models.aplication import AplicationModel


class Parts_Aplications(Resource):
    parser = Req_Parser()
    parser.add_argument('aplication', type=str, required=True)

    # @jwt_required()
    def get(self, part_number):
        parts_aplications = PartAplicationModel.get_list_part_number(
            part_number)
        res = []
        for i in parts_aplications:
            res.append({'aplication': i.json()['aplication']})
        return res, 200

    def put(self, part_number):
        # parser the data to verify if is complete and correct
        ans, data = Parts_Aplications.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # get the attributes
        aplication = request.json['aplication']
        # ask if exist the part_aplication on the DB
        exist_part_aplication = PartAplicationModel.find_equal_value(
            part_number, aplication)
        if exist_part_aplication:
            return {"message": "The part_number with the aplication already exist in DB, but is not a problem"}, 200
        # ask if exist the part_number on the DB
        exist_part_number = PartNumberModel.find_by_part_number(part_number)
        if not exist_part_number:
            PartNumberList.add_part(part_number)
        # ask if exist the aplication on the DB
        exist_aplication = AplicationModel.find_by_aplication(aplication)
        if not exist_aplication:
            _aplication = AplicationModel(aplication)
            _aplication.save_to_db()
        # add part_aplication on the DB
        part_aplication = PartAplicationModel(part_number, aplication)
        try:
            part_aplication.save_to_db()
        except:
            return {'message': "An error has ocurred while adding the part_aplication at BD"}
        return part_aplication.json()

    def delete(self, part_number):
        ans, data = self.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # ask if exist
        part_aplication = PartAplicationModel.find_equal_value(
            part_number, **data)
        if part_aplication:
            part_aplication.delete_from_db()
            return part_aplication.json(), 200

        return {'message': 'Part_Motor not found.'}
