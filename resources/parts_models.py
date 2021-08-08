from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.part_model import PartModel_Model
from models.part_number import PartNumberModel
from models.turbo_model import TurboModel_Model
from resources.part_numbers import PartNumberList
from Req_Parser import Req_Parser


class Parts_Models(Resource):
    parser = Req_Parser()
    parser.add_argument('part_number', type=str, required=True)
    parser.add_argument('model', type=str, required=True)

    # # modules that are
    def add_part_number(part_number):
        ans, data = PartNumberList.add_part(part_number)

    # def add_model(model):

    # def add_part_model(part_number, model):

    # def add_model_in_part_number(part_number, model):
    #     part_model = PartModel_Model.find_equal_value(part_number, model)
    #     if part_model:
    #         return {"message": "The part_number with the model already exist in BD, but is not a problem"}, 200
    #     else:
    #         model = TurboModel_Model.find_by_model(model)
    #         if model:
    #             ans, data = Parts_Models.parser(dict(request.json))
    #             if not ans:
    #                 return data
    #             part_model = PartModel_Model(**data)
    #             try:
    #                 part_model.save_to_db()
    #             except:
    #                 return {'message': "An error has ocurred while adding the part_model at BD"}
    #             return part_model.json(), 201

    # @jwt_required()

    def get(self):
        part_number = request.json['part_number']
        parts_models = PartModel_Model.find_by_part_number(part_number)
        res = []
        for i in parts_models:
            res.append({'model': i.json()['model']})
        return res, 200

    def put(self):
        # parser the data to verify if is complete and correct
        ans, data = Parts_Models.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # get the attributes
        part_number = request.json['part_number']
        model = request.json['model']
        # ask if exist the part_model on the DB
        exist_part_model = PartModel_Model.find_equal_value(part_number, model)
        if exist_part_model:
            return {"message": "The part_number with the model already exist in DB, but is not a problem"}, 200
        # ask if exist the part_number on the DB
        # exist_part_number = Parts_Models.verify_part_number(part_number)
        exist_part_number = PartNumberModel.find_by_part_number(part_number)
        if not exist_part_number:
            # Parts_Models.add_part_number(part_number)
            PartNumberList.add_part(part_number)
            # _part_number = PartNumberModel(part_number)
            # _part_number.save_to_db()
        # ask if exist the model on the DB
            # exist_model = Parts_Models.verify_model()
        exist_model = TurboModel_Model.find_by_model(model)
        if not exist_model:
            _model = TurboModel_Model(model)
            _model.save_to_db()
        # add part_model on the DB
        part_model = PartModel_Model(part_number, model)
        try:
            part_model.save_to_db()
        except:
            return {'message': "An error has ocurred while adding the part_model at BD"}
        return part_model.json()
