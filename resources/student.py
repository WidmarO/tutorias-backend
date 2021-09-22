from re import escape
from flask_restful import Resource
from flask import request
from models.student import StudentModel
from models.tutoring_program import TutoringProgramModel
from models.user import UserModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt

class Student(Resource): #/student
    parser = Req_Parser()    
    parser.add_argument('cod_student', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    parser.add_argument('address')
    parser.add_argument('reference_person')
    parser.add_argument('phone_reference_person')
    # parser.add_argument('cod_tutoring_program', str, True)

    @jwt_required()
    def put(self, cod_student):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
            
        # Verify if all arguments are correct
        ans, data = StudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if student exists in database
        student = StudentModel.find_by_cod_student(cod_student)
        if student:
            try:
                student.update_data(**data)
                student.save_to_db()
            except:
                return {'message': 'An error occurred while updating student'}, 500
            return student.json(), 200
        return {'message': 'Student not found.'}, 404

    @jwt_required()
    def get(self, cod_student):
        # Return a student if found in database
        student = StudentModel.find_by_cod_student(cod_student)
        if student:
            return student.json(), 200
        return {'message': 'Student not found'}, 404

    @jwt_required()
    def delete(self, cod_student):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401   

        # Delete a student from database if exist in it
        student = StudentModel.find_by_cod_student(cod_student)
        if student:
            try:
                student.delete_from_db()
            except:
                return {'message': 'An error occurred while deleting student'}, 500
            return student.json(), 200

        # Return a messagge if not found
        return {'message': 'Student not found.'}, 404


class StudentS(Resource): # /student_update
    parser = Req_Parser()
    parser.add_argument('phone')
    parser.add_argument('address')
    parser.add_argument('reference_person')
    parser.add_argument('phone_reference_person')

    @jwt_required()
    def put(self):
        claims = get_jwt()
        if claims['role'] != 'student':
            return {'message': 'You are not allowed to do this'}, 401
            
        # Verify if all arguments are correct
        ans, data = StudentS.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Get student by email in tutoring program
        email_student = claims["sub"]
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        student = StudentModel.find_email_in_tutoring_program(email_student, tutoring_program.cod_tutoring_program)

        data['cod_student'] = student.cod_student 
        # Verify if student exists in database
        if student:
            try:
                student.update_data_Student(**data)
                student.save_to_db()
            except:
                return {'message': 'An error occurred while updating student'}, 500
            return student.json(), 200
        return {'message': 'Student not found.'}, 404


class StudentList(Resource): # /students
    parser = Req_Parser()    
    parser.add_argument('cod_student', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    parser.add_argument('address', str, True)
    parser.add_argument('reference_person')
    parser.add_argument('phone_reference_person')
    # parser.add_argument('cod_tutoring_program', str, True)
    
    @jwt_required()
    def get(self):
        # Return all students in database        
        sort_students = [ student.json() for student in StudentModel.find_all() ]
        sort_students = sorted(sort_students, key=lambda x: x[list(sort_students[0].keys())[0]])    
        return sort_students, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Verify if all attributes are in request and are of corrects type
        ans, data = StudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if student already exists in database
        cod_student = data['cod_student']        
        if StudentModel.find_by_cod_student(cod_student):
            return {'message': "A student with cod_student: '{}' already exist".format(cod_student)}

        # Get the tutoring program active
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active() 
        data['cod_tutoring_program'] = tutoring_program_active.cod_tutoring_program

        # Create a instance of StudentModel with the data provided
        student = StudentModel(**data)

        # Try to insert the student in database
        try:
            student.save_to_db()
        except:
            return {'message': "An error ocurred when adding the student in DB"}, 500

        # Return the student data with a status code 201
        return student.json(), 201


class StudentListTutoringProgram(Resource): # /studentlist/cod_tutoring_program
    
    @jwt_required()
    def get(self, cod_tutoring_program):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all students in database        
        sort_students_in_tutoring_program = [ student.json() for student in StudentModel.find_by_cod_tutoring_program(cod_tutoring_program) ]
        sort_students_in_tutoring_program = sorted(sort_students_in_tutoring_program, key=lambda x: x[list(sort_students_in_tutoring_program[0].keys())[0]])    
        return sort_students_in_tutoring_program, 200


class AddStudents(Resource): # /students_update
    parser = Req_Parser()
    parser.add_argument('student_list', list, True)
    # for each student:
    # {cod_student, name, f_lastname, m_lastname, email}

    @jwt_required()
    def put(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Verify if all attributes are in request and are of corrects type        
        ans, data = AddStudents.parser.parse_args(dict(request.json))
        if not ans:
            return data
        
        # declare variables to count
        count_students = 0
        count_students_added = 0
        count_students_not_added = 0

        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        for s in data['student_list']:
            count_students += 1
            s['phone'] = ''
            s['address'] = ''
            s['reference_person'] = ''
            s['phone_reference_person'] = '' 

            # verify if student already exists in database
            student = StudentModel.find_student_in_tutoring_program(tutoring_program.cod_tutoring_program, s['cod_student'])
            if not student:
                student = StudentModel(s['cod_student'], s['name'], s['f_lastname'], s['m_lastname'], s['phone'], s['email'], s['address'], s['reference_person'], s['phone_reference_person'], tutoring_program.cod_tutoring_program)
                try:
                    student.save_to_db()
                    count_students_added += 1
                except:
                    return {'message': "An error ocurred when adding the student in DB"}, 500
            else:
                count_students_not_added += 1

            # verify if student_user already exists in database
            student_user = UserModel.find_by_username(s['email'])
            if not student_user:            
                student_user  = UserModel(s['email'], self.create_password_student(s['email']), 'student')
                try:                    
                    student_user.save_to_db()
                except:
                    return {'message': 'An error ocurred while trying add Student and UserStudent in DB'} , 500


        # student_list = [ student.json() for student in StudentModel.find_by_cod_tutoring_program(tutoring_program.cod_tutoring_program)]
        # student_list = sorted(student_list, key=lambda x: x[list(student_list[0].keys())[0]])
        # student_account_list = [ student_user.json() for student_user in UserModel.find_by_role('student')]
        # student_account_list = sorted(student_account_list, key=lambda x: x[list(student_account_list[0].keys())[0]])
        # return student_list, 200

        return {'message': '{} total_students, {} students added, {} students not added'.format(count_students, count_students_added, count_students_not_added)}, 200


    def create_password_student(self, email):
        _string = email
        _string = _string.split('@')
        new_password = _string[0]
        return new_password