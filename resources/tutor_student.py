from models.student import StudentModel
from models.teacher import TeacherModel
from flask_restful import Resource
from flask import request
from models.tutor_student import TutorStudentModel
from models.tutoring_program import TutoringProgramModel
from models.tutor import TutorModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt

class TutorStudent(Resource):

    parser = Req_Parser()    
    parser.add_argument('cod_tutor', str, True)
    parser.add_argument('cod_student', str, True)
    parser.add_argument('cod_tutoring_program', str, True)

    def put(self, cod_tutor):
        # Verify if all attributes are in request and are of correct type
        ans, data = TutorStudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # Create a instance of TutorStudentModel with the data provided
        tutor_student = TutorStudentModel.find_by_cod_tutor(cod_tutor)
        if tutor_student:
            tutor_student.update_data(**data)
            tutor_student.save_to_db()
            return tutor_student.json(), 200
        return {'message': 'tutor_student not found.'}, 404

    def get(self, cod_tutor):
        tutor_student = TutorStudentModel.find_by_cod_tutor(cod_tutor)
        if tutor_student:
            return tutor_student.json(), 200
        return {'message': 'tutor_student not found.'}, 404
    
    def delete(self, cod_tutor):
        '''Delete a tutor_student from database if exist in it'''
        # print(request.json)
        # cod_tutor = request.json['cod_tutor']

        tutor_student = TutorStudentModel.find_by_cod_tutor(cod_tutor)
        if tutor_student:
            tutor_student.delete_from_db()
            return tutor_student.json(), 200

        return {'message': 'tutor_student not found.'}


class TutorStudenList(Resource):

    parser = Req_Parser()
    parser.add_argument('cod_tutor', str, True)
    parser.add_argument('cod_student', str, True)
    parser.add_argument('cod_tutoring_program', str, True)
    # @jwt_required()

    def get(self):
        # Return all tutor_student in database
        sort_tutor_students = [ tutor_student.json() for tutor_student in TutorStudentModel.find_all()]
        sort_tutor_students = sorted(sort_tutor_students, key=lambda x: x[list(sort_tutor_students[0].keys())[0]])
        print(sort_tutor_students)
        return sort_tutor_students
        # return {'message': 'List of tutor_students'}


class TutorStudentT(Resource):

    @jwt_required()
    def get(self):
        
        claims = get_jwt()

        if claims['role'] != 'tutor':
            return {'message': 'You are not allowed to do this'}, 401

        email_teacher=claims['sub']
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        teacher = TeacherModel.find_email_in_tutoring_program(email_teacher, tutoring_program.cod_tutoring_program)
        tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)

        # Get tutoring program
        # Return a teacher if found in database
        sort_tutor_student = [ tutor_student.json() for tutor_student in TutorStudentModel.find_students_by_tutor_in_tutoring_program(tutoring_program.cod_tutoring_program, tutor.cod_tutor) ]
        students_by_tutor = [ StudentModel.find_by_cod_student(student['cod_student']).json() for student in sort_tutor_student ]

        return students_by_tutor, 200


class TutorStudentC(Resource):

    def get(self, cod_tutor, cod_tutoring_program, cod_student):
        # Return a teacher if found in database
        sort_tutor_student = [ tutor_student.json() for tutor_student in TutorStudentModel.find_if_relation_exists_in_tutoring_program(cod_tutor, cod_student, cod_tutoring_program) ]
        return sort_tutor_student, 200
    
    def delete(self, cod_tutor, cod_tutoring_program, cod_student):
        # Delete a student from database if exist in it
        tutor_student = TutorStudentModel.find_if_relation_exists_in_tutoring_program(cod_tutor, cod_student, cod_tutoring_program)
        if tutor_student:
            tutor_student.delete_from_db()
            return tutor_student.json(), 200
        # Return a messagge if not found
        return {'message': 'Student not found.'}, 404  
    
    def put(self, cod_tutor, cod_tutoring_program, cod_student):
        # if request['rol'] != 'admin':
        #     return {'message': 'Admin privilege required.'}, 401
        # Verify if all arguments are correct
        ans, data = TutorStudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if student exists in database
        tutorstudent = TutorStudentModel.find_if_relation_exists_in_tutoring_program(cod_tutor, cod_student,cod_tutoring_program)
        if tutorstudent:
            tutorstudent.update_data(**data)
            tutorstudent.save_to_db()
            return tutorstudent.json(), 200

        return {'message': 'Student not found.'}, 404

class TutorStudentList(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_tutor', str, True)
    parser.add_argument('cod_student', str, True)
    parser.add_argument('cod_tutoring_program', str, True)
    
    # @jwt_required()
    def get(self):
        # Return all relation of the tutor with students in database        
        sort_tutor_student = [ tutor_student.json() for tutor_student in TutorStudentModel.find_all() ]
        sort_tutor_student = sorted(sort_tutor_student, key=lambda x: x[list(sort_tutor_student[0].keys())[0]])
        
        return sort_tutor_student, 200

    def post(self):

        '''Add or created a new tutor_student in database if already them not exist'''
        # Verify if all attributes are in request and are of corrects type
        ans, data = TutorStudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        print(request.json)
        cod_tutor = data['cod_tutor']
        if TutorStudentModel.find_by_cod_tutor(cod_tutor):
            return {'message': "A tutor_student with cod_tutor: '{}' already exist".format(cod_tutor)}

        # Create a instance of TutorStudentModel with the data provided
        tutor_student = TutorStudentModel(**data)

        try:
            tutor_student.save_to_db()
        except:
            return {'message': "An error ocurred adding the tutor_student in DB"}, 500

        return tutor_student.json(), 201
        
        