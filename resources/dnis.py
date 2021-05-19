import requests
from flask_restful import Resource
from flask import request
from Req_Parser import Req_Parser


class DNI(Resource):
    parser = Req_Parser()
    parser.add_argument('dni', str, required=True)

    def post(self):

        url = 'http://api.peruapis.com/v1/dni'

        print(request.json)
        dni = request.json['dni']
        # data = {'document': str(dni)}
        headers = {'Authorization': 'Bearer udyhV3w2wAqEhrrlKGxVoKwGld4ayO7v9bjOtMyXRziLvaZyJ8liONnItPLA',
                   'Accept': 'application/json'}

        response = requests.post(
            url, data={'document': str(dni)}, headers=headers)
        print(response.json())
        return response.json()
