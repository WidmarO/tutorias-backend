from flask_restful import Resource
from flask import request

from models.user import UserModel
from models.coordinator import CoordinatorModel
from Req_Parser import Req_Parser

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt


class UpdateCredentialsCoordinator(Resource):
    parser = Req_Parser()
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone', str)
    parser.add_argument('email', str, True)
    parser.add_argument('before_username', str, True)       
    parser.add_argument('before_password', str, True)
    parser.add_argument('new_username', str, True)
    parser.add_argument('new_password', str, True)

    @jwt_required()
    def put(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        '''Log a user in'''
        ans, data = UpdateCredentialsCoordinator.parser.parse_args(dict(request.json))
        if not ans:
            return data
        
        user = UserModel.find_by_username(data['before_username'])
        if not user:
            return {'message': 'User does not exist'}, 404
        
        # verify if the username already exists
        if UserModel.find_by_username(data['new_username']):
            return {'message': "A user with that username already exist"}, 400
        
        # save the user in the db

        cod_coordinator = self.create_cod_coordinator()
        print(cod_coordinator)
        coordinator = CoordinatorModel.find_by_cod_coordinator(cod_coordinator)
        if not coordinator:
            coordinator = CoordinatorModel(cod_coordinator, data['name'], data['f_lastname'], data['m_lastname'], data['phone'], data['email'])
            try:
                coordinator.save_to_db()
            except:
                return {'message': 'An error ocurred while trying add Coordinator in DB'} , 500
        
        if user.password == data['before_password']:
            print('si entra')
            print('===========================================================')
            user.username = data['new_username']
            user.password = data['new_password']
            user.save_to_db()
            access_token = create_access_token(user.username, additional_claims={'role': user.role, 'id': user.id})
            return {'token': access_token}, 200
        else:
            return {'message': 'Wrong credentials'}, 401  

    def create_cod_coordinator(self):
        list_coordinators = CoordinatorModel.find_all()
        list_coordinators = [ coordinator.json() for coordinator in list_coordinators]
        list_coordinators = sorted(list_coordinators, key=lambda x: x[list(list_coordinators[0].keys())[0]])
        if len(list_coordinators) == 0 :
            return 'CO-001'
        _max = list_coordinators[-1]['cod_coordinator']
        entero=int(_max[-3:])
        new_code = _max[:3] + '{:>03}'.format(str(entero+1))
        return new_code

    def create_password_coordinator(self):
        list_coordinator_accounts = UserModel.find_by_role('coordinator')
        list_coordinator_accounts = [ coordinator_account.json() for coordinator_account in list_coordinator_accounts]
        list_coordinator_accounts = sorted(list_coordinator_accounts, key=lambda x: x[list(list_coordinator_accounts[0].keys())[0]])
        if len(list_coordinator_accounts) == 0 :
            return 'admin'
        _string = list_coordinator_accounts[-1]['username']
        _string = _string.split('@')
        new_password = _string[0]
        return new_password


