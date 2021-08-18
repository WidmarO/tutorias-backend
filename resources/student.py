from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.student import StudentModel
from Req_Parser import Req_Parser

class Student(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('cod_student', esp_attr=True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname')
    parser.add_argument('m_lastname')
    parser.add_argument('phone')
    parser.add_argument('email')
    parser.add_argument('cod_faculty')
    parser.add_argument('cod_career')
    parser.add_argument('adress')
    # @jwt_required()

    def delete(self, cod_student):
        '''Delete a student from database if exist in it'''
        #print(request.json)
        #cod_student = request.json['cod_student']

        student = StudentModel.find_by_cod_student(cod_student)
        if student:
            student.delete_from_db()
            return student.json(), 200

        return {'message': 'Student not found.'}


class StudentList(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('cod_student', esp_attr=True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname')
    parser.add_argument('m_lastname')
    parser.add_argument('phone')
    parser.add_argument('email')
    parser.add_argument('cod_faculty')
    parser.add_argument('cod_career')
    parser.add_argument('adress')
    # @jwt_required()

    def get(self):
        sort_students = list(map(lambda x: x.json(), StudentModel.query.all()))
        sort_students = sorted(sort_students, key=lambda x: x[list(sort_students[0].keys())[0]])
        print(sort_students)
        return sort_students
        # return {'message': 'List of students'}


    def post(self):
        print(request.json)
        cod_student = request.json['cod_student']
        '''Add or created a new student in database if already them not exist'''
        if StudentModel.find_by_cod_student(cod_student):
            return {'message': "A student with cod_student: '{}' already exist".format(cod_student)}

        ans, data = StudentList.parser.parse_args(dict(request.json))

        if not ans:
            return data

        student = StudentModel(**data)

        try:
            student.save_to_db()
        except:
            return {'message': "An error ocurred adding the student"}, 500

        return student.json(), 201

    def delete(self):
        '''Delete a student from database if exist in it'''
        print(request.json)
        cod_student = request.json['cod_student']
        student = StudentModel.find_by_cod_student(cod_student)
        if student:
            student.delete_from_db()
            return student.json(), 200

        return {'message': 'Student not found.'}
