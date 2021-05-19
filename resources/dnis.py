import requests
from flask_restful import Resource
from flask import request
from Req_Parser import Req_Parser


class DNI(Resource):
    parser = Req_Parser()
    parser.add_argument('dni', str, required=True)

    def post(self):
        dni = request.json['dni']
        data = {'document': dni}
        url = 'http://api.peruapis.com/v1/dni'
        headers = {'Authorization': 'Bearer udyhV3w2wAqEhrrlKGxVoKwGld4ayO7v9bjOtMyXRziLvaZyJ8liONnItPLA',
                   'Accept': 'application/json'}
        response = requests.post(url, data=data, headers=headers)
        print(response.json()['data'])
        return response.json()['data']
