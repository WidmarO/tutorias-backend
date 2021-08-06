from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.part_model import PartModel_Model
from models.part_number import PartNumberModel
from models.turbo_model import TurboModel_Model
from Req_Parser import Req_Parser
from db import db

import json


class Turbos(Resource):

    # @jwt_required()
    def get_part_numbers(self):
        sort_turbos = list(
            map(lambda x: x.json(), PartNumberModel.query.all()))
        sort_turbos = sorted(
            sort_turbos, key=lambda x: x[list(sort_turbos[0].keys())[0]])
        print(sort_turbos)
        return sort_turbos

    def get_parts_models(self):
        parts = self.get_part_numbers()
        parts_models = list(
            map(lambda x: x.json(), PartModel_Model.query.all()))
        print("===PARTS===\n", parts)
        print("===PARTS-MODELS===\n", parts_models)

    def get(self):
        results = db.session.query(
            PartNumberModel, PartModel_Model).join(PartNumberModel).all()

        res = []
        for i, j in results:
            ans = {}
            ans['id'] = i.id
            ans['part_number'] = i.part_number
            ans['models'] = []
            if ans not in res:
                res.append(ans)

        for i, j in results:
            for k in res:
                if i.id == k['id'] and j.model not in k['models']:
                    k['models'].append(j.model)

        for i in res:
            i['models'] = ", ".join(i['models'])

        print(res)
        return res

    def post(self):
        # generate the new id for new data
        _list = list(map(lambda x: x.json(), PartNumberModel.query.all()))
        new_id = 0
        for i in _list:
            if i['id'] > new_id:
                new_id = i['id']
        id = new_id + 1

        # ask if in the db already exist a data with the same id
        if PartNumberModel.find_by_id(id):
            return {'message': "A catalogue: '{}' already exist in data base".format(id)}

        # ask if in the db already exist a data with the same part_number
        part_number = request.json['part_number']
        if PartNumberModel.find_by_id(part_number):
            return {'message': "A catalogue: '{}' already exist in data base".format(id)}

        # ask if the request data is complete and with correct values
        ans, data = Turbos.parser.parse_args(dict(request.json))
        print(data)
        if not ans:
            return data

        # get the request values
        r_part_number = request.json['part_number']
        models = request.json['models']
        brands = request.json['brands']
        motors = request.json['motors']
        aplications = request.json['aplications']

        part_number = PartNumberModel(id, r_part_number)
        list_models = []
        for i in models:
            model = TurboModel_Model(i['model'])
            model.save_to_db()
            list_models.append(PartModel_Model(part_number, i['model']))

        try:
            part_number.save_to_db()

            print(model.json)
            for i in list_models:
                print("============si==========")
                i.save_to_db()
                print("============no==========")

        except:
            return {'message': "An error ocurred adding the turbo"}, 500

        turbo = {}
        turbo['id'] = part_number.part_number
        turbo['part_number'] = part_number.part_number
        turbo['models'] = []
        for i in list_models:
            turbo['models'].append({'model': i.model})

        return json.dumps(turbo), 201
