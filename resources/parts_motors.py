from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from Req_Parser import Req_Parser

# Importing the models and other resources requireds
from resources.part_numbers import PartNumberList
from models.part_number import PartNumberModel
from models.part_motor import PartMotorModel
from models.motor import MotorModel


class Parts_Motors(Resource):
    parser = Req_Parser()
    parser.add_argument('motor', type=str, required=True)

    # @jwt_required()
    def get(self, part_number):
        parts_motors = PartMotorModel.get_list_part_number(part_number)
        res = []
        for i in parts_motors:
            res.append({'motor': i.json()['motor']})
        return res, 200

    def put(self, part_number):
        # parser the data to verify if is complete and correct
        ans, data = Parts_Motors.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # get the attributes
        motor = request.json['motor']
        # ask if exist the part_motor on the DB
        exist_part_motor = PartMotorModel.find_equal_value(part_number, motor)
        if exist_part_motor:
            return {"message": "The part_number with the motor already exist in DB, but is not a problem"}, 200
        # ask if exist the part_number on the DB
        exist_part_number = PartNumberModel.find_by_part_number(part_number)
        if not exist_part_number:
            PartNumberList.add_part(part_number)
        # ask if exist the motor on the DB
        exist_motor = MotorModel.find_by_motor(motor)
        if not exist_motor:
            _motor = MotorModel(motor)
            _motor.save_to_db()
        # add part_motor on the DB
        part_motor = PartMotorModel(part_number, motor)
        try:
            part_motor.save_to_db()
        except:
            return {'message': "An error has ocurred while adding the part_motor at BD"}
        return part_motor.json()

    def delete(self, part_number):
        ans, data = self.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # ask if exist
        part_motor = PartMotorModel.find_equal_value(part_number, **data)
        if part_motor:
            part_motor.delete_from_db()
            return part_motor.json(), 200

        return {'message': 'Part_Motor not found.'}
