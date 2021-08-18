# from flask_restful import Resource
# from flask import request
# from flask_jwt import jwt_required
# from models.turbo_model import TurboModel_Model
# from Req_Parser import Req_Parser


# class ModelList(Resource):
#     parser = Req_Parser()

#     parser.add_argument('model', str, True)
#     # @jwt_required()

#     def get(self):
#         sort_models = list(
#             map(lambda x: x.json(), TurboModel_Model.query.all()))
#         sort_models = sorted(
#             sort_models, key=lambda x: x[list(sort_models[0].keys())[0]])
#         print(sort_models)
#         return sort_models

#     def post(self):

#         print(request.json)
#         model = request.json['model']
#         '''Add or created a new model in database if already them not exist'''
#         if TurboModel_Model.find_by_model(model):
#             return {'message': "The model: '{}' already exist in data base".format(model)}

#         ans, data = ModelList.parser.parse_args(dict(request.json))
#         if not ans:
#             return data

#         model = TurboModel_Model(**data)

#         try:
#             model.save_to_db()
#         except:
#             return {'message': "An error ocurred adding the model"}, 500

#         return model.json(), 201

#     def delete(self):
#         '''Delete a model from database if exist in it'''
#         print(request.json)
#         model = request.json['model']
#         model = TurboModel_Model.find_by_model(model)
#         if model:
#             model.delete_from_db()
#             return model.json(), 200

#         return {'message': 'model not found.'}
