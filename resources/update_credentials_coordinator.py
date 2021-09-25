from flask_restful import Resource
from flask import request
import bcrypt
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
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    parser.add_argument('before_username', str, True)       
    parser.add_argument('before_password', str, True)
    parser.add_argument('new_username', str, True)
    parser.add_argument('new_password', str, True)

    @jwt_required()
    def put(self):

        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 402
        # Verify if the request data is correct
        ans, data = UpdateCredentialsCoordinator.parser.parse_args(dict(request.json))
        if not ans:
            return data
        password = data['before_password']
        # Verify if the user exists
        user = UserModel.find_by_username(data['before_username'])
        if not user:
            return {'message': 'User does not exist'}, 404

        new_password = data['new_password']
        new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        # Verify if the before password is correct
        if not (bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
            user.username = new_hashed
            return {'message': 'The before credentials are wrong'}, 401

        # Verify if the new username already exists
        if UserModel.find_by_username(data['new_username']):
            return {'message': "A user with the new username already exist"}, 400
        
        # Create new code for the coordinator
        cod_coordinator = self.create_cod_coordinator()        
        # coordinator = CoordinatorModel.find_by_cod_coordinator(cod_coordinator)
        coordinator = CoordinatorModel(cod_coordinator, data['name'], data['f_lastname'], data['m_lastname'], data['phone'], data['email'])
        try:
            # Save the user coordinator in the db
            coordinator.save_to_db()
        except:
            return {'message': 'An error ocurred while trying add Coordinator in DB'} , 500

        # Update credentials of the user            
        user.username = data['new_username']
        user.password = new_hashed
        try:
            user.save_to_db()
        except:
            return {'message': 'An error ocurred while trying update the credentials in DB'} , 500

        # Return the token JWT with new credentials
        access_token = create_access_token(user.username, additional_claims={'role': user.role, 'id': user.id})
        return {'token': access_token, 'message': "Cordinator credentials update correctly, logout and login with new credentials"}, 200


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

    # def create_password_coordinator(self):
    #     list_coordinator_accounts = UserModel.find_by_role('coordinator')
    #     list_coordinator_accounts = [ coordinator_account.json() for coordinator_account in list_coordinator_accounts]
    #     list_coordinator_accounts = sorted(list_coordinator_accounts, key=lambda x: x[list(list_coordinator_accounts[0].keys())[0]])
    #     if len(list_coordinator_accounts) == 0 :
    #         return 'admin'
    #     _string = list_coordinator_accounts[-1]['username']
    #     _string = _string.split('@')
    #     new_password = _string[0]
    #     return new_password


