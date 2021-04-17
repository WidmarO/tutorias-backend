from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.employee import EmployeeModel
from Req_Parser import Req_Parser


class Employee(Resource):
    parser = Req_Parser()
    parser.add_argument('dni', str, required=True)
    parser.add_argument('name', str,  required=True)
    parser.add_argument('f_lastname')
    parser.add_argument('m_lastname')
    parser.add_argument('age')
    parser.add_argument('gender')
    parser.add_argument('address')
    parser.add_argument('phone')
    parser.add_argument('email')

    # @jwt_required()
    def get(self, dni):
        '''Search employee by name in the database and return it if is founded'''
        employee = EmployeeModel.find_by_dni(dni)
        if employee:
            return employee.json()
        return {'message': 'employee not found'}, 404

    def put(self, dni):

        ans, data = Employee.parser.parse_args(dict(request.json))
        if not ans:
            return data

        employee = EmployeeModel.find_by_dni(dni)

        if employee:
            employee.update_data(**data)

        else:
            return {'message': "employee not found."}

        employee.save_to_db()
        employee_list = EmployeeList()
        return employee_list.get()


class EmployeeList(Resource):
    parser = Req_Parser()
    parser.add_argument('dni', str, required=True)
    parser.add_argument('name', str,  required=True)
    parser.add_argument('f_lastname')
    parser.add_argument('m_lastname')
    parser.add_argument('age')
    parser.add_argument('gender')
    parser.add_argument('address')
    parser.add_argument('phone')
    parser.add_argument('email')
    # @jwt_required()

    def get(self):
        return list(map(lambda x: x.json(), EmployeeModel.query.all()))

    def post(self):
        print(request.json)
        dni = request.json['dni']
        '''Add or created a new employee in database if already them not exist'''
        if EmployeeModel.find_by_dni(dni):
            return {'message': "A employee with dni: '{}' already exist".format(dni)}

        ans, data = Employee.parser.parse_args(dict(request.json))
        if not ans:
            return data

        employee = EmployeeModel(**data)

        try:
            employee.save_to_db()
        except:
            return {'message': "An error ocurred adding the employee"}, 500

        return employee.json(), 201

    def delete(self):
        '''Delete a employee from database if exist in it'''
        print(request.json)
        dni = request.json['dni']
        employee = EmployeeModel.find_by_dni(dni)
        if employee:
            employee.delete_from_db()
            return employee.json(), 200

        return {'message': 'employee not found.'}
