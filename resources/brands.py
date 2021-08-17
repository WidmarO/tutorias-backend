from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.brand import BrandModel
from Req_Parser import Req_Parser


class BrandList(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('brand', str, True)
    # @jwt_required()

    def get(self):
        # sort_brands = list(
        #     map(lambda x: x.json(), BrandModel.query.all()))
        # sort_brands = sorted(
        #     sort_brands, key=lambda x: x[list(sort_brands[0].keys())[0]])
        # print(sort_brands)
        # return sort_brands

        return {'message': 'List of brands'}


    def post(self):

        print(request.json)
        brand = request.json['brand']
        '''Add or created a new brand in database if already them not exist'''
        if BrandModel.find_by_brand(brand):
            return {'message': "A brand: '{}' already exist in data base".format(brand)}

        ans, data = BrandList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        brand = BrandModel(**data)

        try:
            brand.save_to_db()
        except:
            return {'message': "An error ocurred adding the brand"}, 500

        return brand.json(), 201

    def delete(self):
        '''Delete a brand from database if exist in it'''
        print(request.json)
        brand = request.json['brand']
        brand = BrandModel.find_by_brand(brand)
        if brand:
            brand.delete_from_db()
            return brand.json(), 200

        return {'message': 'Brand not found.'}
