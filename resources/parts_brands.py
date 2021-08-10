from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from Req_Parser import Req_Parser

# Importing the models and other resources requireds
from models.part_brand import PartBrandModel
from models.part_number import PartNumberModel
from models.brand import BrandModel
from resources.part_numbers import PartNumberList


class Parts_Brands(Resource):
    parser = Req_Parser()
    parser.add_argument('brand', type=str, required=True)

    # @jwt_required()
    def get(self, part_number):
        parts_brands = PartBrandModel.get_list_part_number(part_number)
        res = []
        for i in parts_brands:
            res.append({'brand': i.json()['brand']})
        return res, 200

    def put(self, part_number):
        # parser the data to verify if is complete and correct
        ans, data = Parts_Brands.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # get the attributes
        brand = request.json['brand']
        # ask if exist the part_brand on the DB
        exist_part_brand = PartBrandModel.find_equal_value(part_number, brand)
        if exist_part_brand:
            return {"message": "The part_number with the brand already exist in DB, but is not a problem"}, 200
        # ask if exist the part_number on the DB
        exist_part_number = PartNumberModel.find_by_part_number(part_number)
        if not exist_part_number:
            PartNumberList.add_part(part_number)
        # ask if exist the brand on the DB
        exist_brand = BrandModel.find_by_brand(brand)
        if not exist_brand:
            _brand = BrandModel(brand)
            _brand.save_to_db()
        # add part_brand on the DB
        part_brand = PartBrandModel(part_number, brand)
        try:
            part_brand.save_to_db()
        except:
            return {'message': "An error has ocurred while adding the part_brand at BD"}
        return part_brand.json()

    def delete(self, part_number):
        ans, data = self.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # ask if exist
        part_brand = PartBrandModel.find_equal_value(part_number, **data)
        if part_brand:
            part_brand.delete_from_db()
            return part_brand.json(), 200

        return {'message': 'Part_Brand not found.'}
