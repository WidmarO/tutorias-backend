from flask_restful import Resource
from flask import request
from models.user import UserModel
from Req_Parser import Req_Parser
import bcrypt
from models.tutoring_program import TutoringProgramModel

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt


# class UserRegister(Resource):
  
#   parser = Req_Parser()
#   parser.add_argument('username', str, True)
#   parser.add_argument('password', str, True)
#   parser.add_argument('role', str, True)
  
  # def post(self):
  #   '''Add a user in a db'''
  #   # verify if the request data is valid
  #   ans, data = UserRegister.parser.parse_args(dict(request.json))
  #   if not ans:
  #     return data
  #   # verify if the username already exists
  #   if UserModel.find_by_username(data['username']):
  #     return {'message': "A user with that username already exist"}, 400
  #   # save the user in the db
  #   user = UserModel(data['username'], data['password'], data['role'])
  #   user.save_to_db()
  #   # create a token for the user
  #   access_token = create_access_token(user.username, additional_claims={'role': user.role, 'id': user.id})
  #   # return token
  #   return {'token': access_token}

class Admin(Resource):

  def post(self):
    username = 'admin'
    password = 'admin'
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = UserModel(username, hashed, 'coordinator')
    user.save_to_db()
    return user.json(), 200


class Login(Resource): # /login
  parser = Req_Parser()
  parser.add_argument('username', str, True)
  parser.add_argument('password', str, True)

  def post(self):
    '''Log a user in'''
    # Verify if the request data is valid
    ans, data = Login.parser.parse_args(dict(request.json))
    if not ans:
      return data    
    password = data['password']

    # Verify if the user exists
    user = UserModel.find_by_username(data['username'])
    if not user:
      return {'message': 'User does not exist'}, 404

    tutoring_program_active = TutoringProgramModel.find_tutoring_program_active()
    if tutoring_program_active:
      # Verify if the password is correct
      if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # Create a token for the user
        access_token = create_access_token(user.username, additional_claims={'role': user.role, 'id': user.id})
        return {'token': access_token}
      else:
        return {'message': 'Wrong credentials'}, 401
    else:
      if user.role == 'coordinator':
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
          access_token = create_access_token(user.username, additional_claims={'role': user.role, 'id': user.id})
          return {'token': access_token}
        else:
          return {'message': 'Wrong credentials'}, 401
      else:
        return {'message': 'There is no active tutoring program, wait that the coordinator active the plan of tutoring program. Thanks.'}, 401

  # @jwt_required()
  # def get(self):
  #   claims = get_jwt()
  #   print("===============================================================")
  #   print(claims)
  #   return {'message': 'You are logged in', 'role':claims['role'], 'username':claims['sub'], 'id':claims['id']}, 200

class UpdateCredentials(Resource):
  parser = Req_Parser()
  parser.add_argument('username', str, True)
  parser.add_argument('password', str, True)
  parser.add_argument('new_password', str, True)

  def put(self):
    '''Log a user in'''
    # Verify if the request data is valid
    ans, data = UpdateCredentials.parser.parse_args(dict(request.json))
    if not ans:
      return data

    # Verify if the user exists
    user = UserModel.find_by_username(data['username'])
    if not user:
      return {'message': 'User does not exist'}, 404
    # Verify if the password is correct
    password = data['password']
    new_password = data['new_password']
    new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
      # Update the password
      user.password = new_hashed
      user.save_to_db()
      # Create a token for the user with new credentials
      access_token = create_access_token(user.username, additional_claims={'role': user.role, 'id': user.id})
      return {'token': access_token}
    else:
      return {'message': 'Wrong credentials'}, 401
