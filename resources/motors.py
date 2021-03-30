from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.motor import MotorModel
from Req_Parser import Req_Parser


class MotorList(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('motor', str, True)
    # @jwt_required()

    def get(self):
        sort_motors = list(
            map(lambda x: x.json(), MotorModel.query.all()))
        sort_motors = sorted(
            sort_motors, key=lambda x: x[list(sort_motors[0].keys())[0]])
        print(sort_motors)
        return sort_motors

    def post(self):

        print(request.json)
        motor = request.json['motor']
        '''Add or created a new motor in database if already them not exist'''
        if MotorModel.find_by_motor(motor):
            return {'message': "A motor: '{}' already exist in data base".format(motor)}

        ans, data = MotorList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        motor = MotorModel(**data)

        try:
            motor.save_to_db()
        except:
            return {'message': "An error ocurred adding the motor"}, 500

        return motor.json(), 201

    def delete(self):
        '''Delete a motor from database if exist in it'''
        print(request.json)
        motor = request.json['motor']
        motor = MotorModel.find_by_motor(motor)
        if motor:
            motor.delete_from_db()
            return motor.json(), 200

        return {'message': 'Motor not found.'}
