from flask_restful import Resource
from flask import request

from models.user import UserModel
from models.tutoring_program import TutoringProgramModel
from models.student import StudentModel
from models.teacher import TeacherModel
from models.tutor import TutorModel
from models.student_helper import StudentHelperModel
from models.coordinator import CoordinatorModel
from models.principal import PrincipalModel
from Req_Parser import Req_Parser

from flask_jwt_extended import jwt_required, get_jwt


class User(Resource):

    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] == 'tutor':
            email_teacher=claims['sub']
            tutoring_program = TutoringProgramModel.find_tutoring_program_active()
            teacher = TeacherModel.find_email_in_tutoring_program(email_teacher, tutoring_program.cod_tutoring_program)
            if not teacher:
                return {'message': 'Teacher not found.'}, 404
            tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)
            if tutor:
                return teacher.json(), 200
            return {'message': 'Tutor not found.'}, 404

        if claims['role'] == 'coordinator':
            email_coordinator=claims['sub']
            coordinator = CoordinatorModel.find_email_in_tutoring_program(email_coordinator)
            if coordinator:
                return coordinator.json(), 200
            return {'message': 'Coordinator not found'}, 404

        if claims['role'] == 'student':
            email_student=claims['sub']
            tutoring_program = TutoringProgramModel.find_tutoring_program_active()
            student = StudentModel.find_email_in_tutoring_program(email_student, tutoring_program.cod_tutoring_program)
            if student:
                return student.json(), 200
            return {'message': 'Student not found.'}, 404

        if claims['role'] == 'principal':
            email_principal=claims['sub']
            tutoring_program = TutoringProgramModel.find_tutoring_program_active()
            teacher = TeacherModel.find_email_in_tutoring_program(email_principal, tutoring_program.cod_tutoring_program)
            if not teacher:
                return {'message': 'Teacher not found.'}, 404
            principal = PrincipalModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)
            # principal = PrincipalModel.find_email(email_principal, tutoring_program.cod_tutoring_program)
            if principal:
                return principal.json(), 200
            return {'message': "Principal not found."}, 404

        if claims['role'] == 'student_helper':
            email_student=claims['sub']
            tutoring_program = TutoringProgramModel.find_tutoring_program_active()
            student = StudentModel.find_email_in_tutoring_program(email_student, tutoring_program.cod_tutoring_program)
            if not student:
                return {"message": "Student not found."}, 404
            student_helper = StudentHelperModel.find_student_in_tutoring_program(tutoring_program.cod_tutoring_program, student.cod_student)
            if student_helper :
                return student_helper.json(), 200
            return {"message": "Student Helper not found."}, 404
    