from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.category import CategoryModel
from Req_Parser import Req_Parser


class CategoryList(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('category', str, True)
    # @jwt_required()

    def get(self):
        sort_categories = list(
            map(lambda x: x.json(), CategoryModel.query.all()))
        sort_categories = sorted(
            sort_categories, key=lambda x: x[list(sort_categories[0].keys())[0]])
        print(sort_categories)
        return sort_categories

    def post(self):

        print(request.json)
        category = request.json['category']
        '''Add or created a new category in database if already them not exist'''
        if CategoryModel.find_by_category(category):
            return {'message': "A category: '{}' already exist in data base".format(category)}

        ans, data = CategoryList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        category = CategoryModel(**data)

        try:
            category.save_to_db()
        except:
            return {'message': "An error ocurred adding the category"}, 500

        return category.json(), 201

    def delete(self):
        '''Delete a category from database if exist in it'''
        print(request.json)
        category = request.json['category']
        category = CategoryModel.find_by_category(category)
        if category:
            category.delete_from_db()
            return category.json(), 200

        return {'message': 'category not found.'}
