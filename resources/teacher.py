from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.teacher import TeacherModel
from Req_Parser import Req_Parser

class Teacher(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('cod_teacher', esp_attr=True)
    parser.add_argument('name')
    parser.add_argument('f_lastname')
    parser.add_argument('m_lastname')
    parser.add_argument('phone')
    parser.add_argument('email')
    

    # @jwt_required()
    def delete(self, cod_teach):
        '''Delete a teacher from database if exist in it'''
        # print(request.json)
        # cod_teach = request.json['cod_teacher']
        teacher = TeacherModel.find_by_cod_teacher(cod_teach)
        if teacher:
            teacher.delete_from_db()
            return teacher.json(), 200

        return {'message': 'Teacher not found.'}


class TeacherList(Resource):
    parser = Req_Parser()
    # parser.add_argument('id', esp_attr=True)
    parser.add_argument('cod_teacher', esp_attr=True)
    parser.add_argument('name')
    parser.add_argument('f_lastname')
    parser.add_argument('m_lastname')
    parser.add_argument('phone')
    parser.add_argument('email')

    # @jwt_required()

    def get(self):
        sort_teachers = list(map(lambda x: x.json(), TeacherModel.query.all()))
        sort_teachers = sorted(sort_teachers, key=lambda x: x[list(sort_teachers[0].keys())[0]])
        print(sort_teachers)
        return sort_teachers

        #return {'message': 'List of teachers'}


    def post(self):

        print(request.json)
        cod_teacher = request.json['cod_teacher']
        '''Add or created a new teacher in database if already them not exist'''
        if TeacherModel.find_by_cod_teacher(cod_teacher):
            return {'message': "A teacher: '{}' already exist in data base".format(cod_teacher)}

        ans, data = TeacherList.parser.parse_args(dict(request.json))
        if not ans:
            return data 

        teacher = TeacherModel(**data)
  
        try:
            teacher.save_to_db()
        except:
            return {'message': "An error ocurred adding a teacher"}, 500

        return teacher.json(), 201

    def delete(self):
        '''Delete a teacher from database if exist in it'''
        print(request.json)
        cod_teach = request.json['cod_teacher']
        teacher = TeacherModel.find_by_cod_teacher(cod_teach)
        if teacher:
            teacher.delete_from_db()
            return teacher.json(), 200

        return {'message': 'Teacher not found.'}
