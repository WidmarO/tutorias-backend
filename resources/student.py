from flask_restful import Resource
from flask import request
from models.student import StudentModel
from Req_Parser import Req_Parser


class Student(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_student', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    parser.add_argument('reference_person')
    parser.add_argument('phone_reference_person')
    parser.add_argument('cod_tutoring_program', str, True)

    def put(self, cod_student):
        # if request['rol'] != 'admin':
        #     return {'message': 'Admin privilege required.'}, 401
        # Verify if all arguments are correct
        ans, data = StudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if student exists in database
        student = StudentModel.find_by_cod_student(cod_student)
        if student:
            student.update_data(**data)
            student.save_to_db()
            return student.json(), 200

        return {'message': 'Student not found.'}, 404

    def get(self, cod_student):
        # Return a student if found in database
        student = StudentModel.find_by_cod_student(cod_student)
        if student:
            return student.json(), 200
        return {'message': 'Student not found'}, 404

    # @jwt_required()
    def delete(self, cod_student):

        # Delete a student from database if exist in it
        student = StudentModel.find_by_cod_student(cod_student)
        if student:
            student.delete_from_db()
            return student.json(), 200

        # Return a messagge if not found
        return {'message': 'Student not found.'}, 404


class StudentList(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_student', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    parser.add_argument('reference_person')
    parser.add_argument('phone_reference_person')
    parser.add_argument('cod_tutoring_program', str, True)
    
    # @jwt_required()
    def get(self):
        # Return all students in database        
        sort_students = [ student.json() for student in StudentModel.find_all() ]
        sort_students = sorted(sort_students, key=lambda x: x[list(sort_students[0].keys())[0]])
        
        return sort_students, 200


    def post(self):

        # Verify if all attributes are in request and are of corrects type
        ans, data = StudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if student already exists in database
        cod_student = data['cod_student']        
        if StudentModel.find_by_cod_student(cod_student):
            return {'message': "A student with cod_student: '{}' already exist".format(cod_student)}

        # Create a instance of StudentModel with the data provided
        student = StudentModel(**data)

        # Try to insert the student in database
        try:
            student.save_to_db()
        except:
            return {'message': "An error ocurred when adding the student in DB"}, 500

        # Return the student data with a status code 201
        return student.json(), 201

