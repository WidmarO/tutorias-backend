from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.client import ClientModel
from Req_Parser import Req_Parser


class Client(Resource):
    parser = Req_Parser()
    parser.add_argument('dni', esp_attr=True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname')
    parser.add_argument('m_lastname')
    parser.add_argument('phone')
    parser.add_argument('email')

    # @jwt_required()
    def get(self, dni):
        '''Search client by name in the database and return it if is founded'''
        client = ClientModel.find_by_dni(dni)
        if client:
            return client.json()
        return {'message': 'client not found'}, 404

    # def post(self, dni):
    #     print(request.json)
    #     '''Add or created a new client in database if already them not exist'''
    #     if ClientModel.find_by_dni(dni):
    #         return {'message': "A client with dni: '{}' already exist".format(dni)}

    #     ans, data = Client.parser.parse_args(dict(request.json))
    #     if not ans:
    #         return data

    #     client = ClientModel(dni, **data)

    #     try:
    #         client.save_to_db()
    #     except:
    #         return {'message': "An error ocurred adding the client"}, 500

    #     return client.json(), 201

    # def delete(self, dni):
    #     '''Delete a client from database if exist in it'''
    #     client = ClientModel.find_by_dni(dni)
    #     if client:
    #         client.delete_from_db()
    #         return client.json(), 200

    #     return {'message': 'Client not found.'}

    # def put(self, dni):

    #     ans, data = Client.parser.parse_args(dict(request.json))
    #     if not ans:
    #         return data

    #     client = ClientModel.find_by_dni(dni)

    #     if client:
    #         client.update_data(**data)

    #     else:
    #         return {'message': "client not found."}

    #     client.save_to_db()
    #     client_list = ClientList()
    #     return client_list.get()


class ClientList(Resource):
    # @jwt_required()
    def get(self):
        return list(map(lambda x: x.json(), ClientModel.query.all()))

    def post(self):
        print(request.json)
        dni = request.json['dni']
        '''Add or created a new client in database if already them not exist'''
        if ClientModel.find_by_dni(dni):
            return {'message': "A client with dni: '{}' already exist".format(dni)}

        ans, data = Client.parser.parse_args(dict(request.json))
        if not ans:
            return data

        client = ClientModel(**data)

        try:
            client.save_to_db()
        except:
            return {'message': "An error ocurred adding the client"}, 500

        return client.json(), 201

    def delete(self):
        '''Delete a client from database if exist in it'''
        dni = request.json['dni']
        client = ClientModel.find_by_dni(dni)
        if client:
            client.delete_from_db()
            return client.json(), 200

        return {'message': 'Client not found.'}
