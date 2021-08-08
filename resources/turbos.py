from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.part_model import PartModel_Model
from models.part_number import PartNumberModel
from models.turbo_model import TurboModel_Model
from Req_Parser import Req_Parser
from db import db


class Turbos(Resource):

    # @jwt_required()
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
