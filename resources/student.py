from re import escape
from flask_restful import Resource
from flask import app, request
from models.student import StudentModel
from models.tutoring_program import TutoringProgramModel
from models.tutor_student import TutorStudentModel
from models.appointment import AppointmentModel
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
    parser.add_argument('is_private')

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
        is_private = data['is_private']
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active()
        student = StudentModel.find_email_in_tutoring_program(email_student, tutoring_program_active.cod_tutoring_program)
        
        if is_private == 'true' and student:
            before_code_tutoring_program = self.Find_Student_in_before_tutoring_program(student.cod_student)
            print('----------------------')
            print(before_code_tutoring_program)
            current_tutor_of_student = TutorStudentModel.find_tutor_by_student_in_tutoring_program(tutoring_program_active.cod_tutoring_program, student.cod_student)
            print('------------------------')
            print(current_tutor_of_student)
            if not current_tutor_of_student:
                return {'message': "A student with cod_student: '{}' not has tutor in current tutoring program. ".format(student.cod_student)}  
            before_tutor_of_student = TutorStudentModel.find_tutor_by_student_in_tutoring_program(before_code_tutoring_program, student.cod_student)
            if not before_tutor_of_student:
                return {'message': "A student with cod_student: '{}' not has tutor in current tutoring program. ".format(student.cod_student)} 
            print('---------------------------')
            print(before_tutor_of_student)
            appointment = AppointmentModel.find_appointment_of_student_in_tutoring_program_first(before_tutor_of_student.cod_student, before_tutor_of_student.cod_tutor, before_code_tutoring_program)
            print('-------------------------')
            print(appointment)
            if not appointment:
                return {'message': "The appointment with cod_student: '{}' not exist in DB in before tutoring program. ".format(student.cod_student)} 
            try:
                # cod_appointment, cod_tutor, cod_student,general_description,private_description,diagnosis,cod_tutoring_program
                appointment.update_data(appointment.cod_appointment, current_tutor_of_student.cod_tutor , current_tutor_of_student.cod_student, appointment.general_description, appointment.private_description, appointment.diagnosis, tutoring_program_active.cod_tutoring_program)
                appointment.save_to_db()
            except:
                return {'message': 'An error occurred while updating appointment'}, 500

        data['cod_student'] = student.cod_student 
        # Verify if student exists in database
        if student:
            try:
                # cod_student, phone, address, reference_person, phone_reference_person
                student.update_data_Student(data['cod_student'], data['phone'], data['address'], data['reference_person'], data['phone_reference_person'] )
                student.save_to_db()
            except:
                return {'message': 'An error occurred while updating student'}, 500
            return student.json(), 200
        return {'message': 'Student not found.'}, 404
    
    def Find_Student_in_before_tutoring_program(self, cod_student):
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active()
        list_tutoring_program = [ tutoring_program.cod_tutoring_program for tutoring_program in TutoringProgramModel.find_all()]
        list_tutoring_program = sorted(list_tutoring_program)
        list_tutoring_program.remove(tutoring_program_active.cod_tutoring_program)

        list_tutoring_program = list_tutoring_program[::-1]
        if len(list_tutoring_program) == 0:
            return tutoring_program_active.cod_tutoring_program
        for t in list_tutoring_program:
            student = StudentModel.find_student_in_tutoring_program(t, cod_student)
            if student:
                before_core_tutoring_program = student.cod_tutoring_program
                return before_core_tutoring_program
            else:
                if StudentModel.find_student_in_tutoring_program(tutoring_program_active.cod_tutoring_program, cod_student):
                    return tutoring_program_active.cod_tutoring_program
                else: 
                    return "Student not exist in DB"


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
    

        


class StudentListTutoringProgram(Resource): # /student_list/<cod_tutoring_program>
    
    @jwt_required()
    def get(self, cod_tutoring_program):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all students in database        
        sort_students_in_tutoring_program = [ student.json() for student in StudentModel.find_by_cod_tutoring_program(cod_tutoring_program) ]
        sort_students_in_tutoring_program = sorted(sort_students_in_tutoring_program, key=lambda x: x[list(sort_students_in_tutoring_program[0].keys())[0]])    
        return sort_students_in_tutoring_program, 200


class AddStudents(Resource): # /addstudents
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


class StudentListPrincipal(Resource): # /student_list_principal
    
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] != 'principal':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all students in database      
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active()  
        sort_students_in_tutoring_program = [ student.json() for student in StudentModel.find_by_cod_tutoring_program(tutoring_program_active.cod_tutoring_program) ]
        sort_students_in_tutoring_program = sorted(sort_students_in_tutoring_program, key=lambda x: x[list(sort_students_in_tutoring_program[0].keys())[0]])    
        return sort_students_in_tutoring_program, 200