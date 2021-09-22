from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt

from models.tutoring_program import TutoringProgramModel
from models.student import StudentModel
from models.teacher import TeacherModel
from models.tutor import TutorModel
from models.student_helper import StudentHelperModel
from models.coordinator import CoordinatorModel
from models.principal import PrincipalModel


class User(Resource): # /authenticate_user

    @jwt_required()
    def get(self):
        # Get the user's id from the JWT
        claims = get_jwt()
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active() 
        # Get the user if the role is tutor
        if claims['role'] == 'tutor':
            email_teacher = claims['sub']            
            # Find teacher by email in tutoring program
            teacher = TeacherModel.find_teacher_by_email_in_tutoring_program(email_teacher, tutoring_program_active.cod_tutoring_program)
            if not teacher:
                return {'message': "Teacher with email: '{}' not found.".format(email_teacher)}, 404
            # Find tutor by cod_teacher in tutoring program
            tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program_active.cod_tutoring_program, teacher.cod_teacher)
            if tutor:
                ans = dict(tutor.json())
                ans['role'] = 'tutor'
                ans['username'] = email_teacher
                return ans, 200
            return {"message": "The teacher is not a tutor"}, 404

        # Get the user if the role is coordinator
        if claims['role'] == 'coordinator':
            email_coordinator = claims['sub']
            coordinator = CoordinatorModel.find_email_in_tutoring_program(email_coordinator)
            if coordinator:
                ans = dict(coordinator.json())
                ans['role'] = 'coordinator'
                ans['username'] = email_coordinator
                return ans, 200
            return {'message': 'Coordinator not found'}, 404
        
        # Get the user if the role is student
        if claims['role'] == 'student':
            email_student = claims['sub']
            student = StudentModel.find_email_in_tutoring_program(email_student, tutoring_program_active.cod_tutoring_program)
            if student:
                ans = dict(student.json())
                ans['role'] = 'student'
                ans['username'] = email_student
                return ans, 200
            return {'message': 'Student not found.'}, 404
        
        # Get the user if the role is principal
        if claims['role'] == 'principal':
            email_principal = claims['sub']
            teacher = PrincipalModel.find_email(email_principal,tutoring_program_active.cod_tutoring_program)
            if not teacher:
                return {'message': 'Teacher not found.'}, 404
            principal = PrincipalModel.find_teacher_in_tutoring_program(tutoring_program_active.cod_tutoring_program, teacher.cod_teacher)    
            if principal:
                ans = dict(principal.json())
                ans['role'] = 'principal'
                ans['username'] = email_principal
                return ans, 200
            return {'message': "Principal not found."}, 404

        # Get the user if the role is student helper
        if claims['role'] == 'student_helper':
            email_student = claims['sub']            
            student = StudentModel.find_email_in_tutoring_program(email_student, tutoring_program_active.cod_tutoring_program)
            if not student:
                return {"message": "Student not found."}, 404
            student_helper = StudentHelperModel.find_student_in_tutoring_program(tutoring_program_active.cod_tutoring_program, student.cod_student)
            if student_helper :
                ans = dict(student_helper.json())
                ans['role'] = 'student_helper'
                ans['username'] = email_student
                return ans, 200
            return {"message": "Student Helper not found."}, 404
    