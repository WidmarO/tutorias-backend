from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.product import ProductModel
from Req_Parser import Req_Parser
import functools


class Product(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('part_number', str, required=True)
    parser.add_argument('category', str, required=True)
    parser.add_argument('stock', int, required=True)
    parser.add_argument('purchase_price', float)
    parser.add_argument('sale_price', float)

    # @jwt_required()
    def get(self, id):
        '''Search product by name in the database and return it if is founded'''
        catalogue = ProductModel.find_by_id(id)
        if catalogue:
            return catalogue.json()
        return {'message': 'catalogue not found'}, 404

    def put(self, id):

        ans, data = ProductList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        catalogue = ProductModel.find_by_id(id)

        if catalogue:
            catalogue.update_data(**data)
        else:
            return {'message': "catalogue not found."}

        catalogue.save_to_db()
        catalogue_list = ProductList()
        return catalogue_list.get()

    def delete(self, id):
        '''Delete a product index from database if exist in it'''
        product = ProductModel.find_by_id(id)
        if product:
            product.delete_from_db()
            return product.json(), 200

        return {'message': 'Client not found.'}


class ProductList(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('part_number', str, required=True)
    parser.add_argument('category', str, required=True)
    parser.add_argument('stock', int, required=True)
    parser.add_argument('purchase_price', float)
    parser.add_argument('sale_price', float)

    # @jwt_required()
    def get(self):
        sort_products = list(
            map(lambda x: x.json(), ProductModel.query.all()))
        sort_products = sorted(
            sort_products, key=lambda x: x[list(sort_products[0].keys())[0]])
        print(sort_products)
        return sort_products

    def post(self):
        print(request.json)
        part_number = request.json['part_number']
        category = request.json['category']
        stock = request.json['stock']
        purchase_price = request.json['purchase_price']
        sale_price = request.json['sale_price']
        '''Add or created a new product in database if already them not exist'''
        if ProductModel.find_by_id(id):
            return {'message': "A product: '{}' already exist in data base".format(id)}

        ans, data = ProductList.parser.parse_args(dict(request.json))

        if not ans:
            return data

        product = ProductModel(**data)

        try:
            product.save_to_db()
        except:
            return {'message': "An error ocurred adding the product"}, 500

        return product.json(), 201
