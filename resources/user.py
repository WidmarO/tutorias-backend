from flask_restful import Resource
from flask import request

from models.user import UserModel
from Req_Parser import Req_Parser

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt



class UserRegister(Resource):
  
  parser = Req_Parser()
  parser.add_argument('username', str, True)
  parser.add_argument('password', str, True)
  parser.add_argument('role', str, True)
  
  def post(self):
    '''Add a user in a db'''
    # verify if the request data is valid
    ans, data = UserRegister.parser.parse_args(dict(request.json))
    if not ans:
      return data
    # verify if the username already exists
    if UserModel.find_by_username(data['username']):
      return {'message': "A user with that username already exist"}
    # save the user in the db
    user = UserModel(data['username'], data['password'], data['role'])
    user.save_to_db()
    # create a token for the user
    access_token = create_access_token(user.username, additional_claims={'role': user.role, 'id': user.id})
    # return token
    return {'token': access_token}

  @jwt_required()
  def get(self):
        return {'message': 'You are logged in'}, 200


class Login(Resource):
  parser = Req_Parser()
  parser.add_argument('username', str, True)
  parser.add_argument('password', str, True)
  
  def post(self):
    '''Log a user in'''
    ans, data = Login.parser.parse_args(dict(request.json))
    if not ans:
      return data

    user = UserModel.find_by_username(data['username'])
    if not user:
      return {'message': 'User does not exist'}, 404

    if user.password == data['password']:
      access_token = create_access_token(user.username, additional_claims={'role': user.role, 'id': user.id})
      return {'token': access_token}
    else:
      return {'message': 'Wrong credentials'}, 401

  @jwt_required()
  def get(self):
    claims = get_jwt()
    print("===============================================================")
    print(claims)
    return {'message': 'You are logged in', 'role':claims['role'], 'username':claims['sub']}, 200

