from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt

from models.tutoring_program import TutoringProgramModel
from models.student import StudentModel
from models.teacher import TeacherModel
from models.tutor import TutorModel
from models.student_helper import StudentHelperModel
from models.coordinator import CoordinatorModel
from models.principal import PrincipalModel


class User(Resource):

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
                return teacher.json(), 200
            return {"message": "The teacher is not a tutor"}, 404

        # Get the user if the role is coordinator
        if claims['role'] == 'coordinator':
            email_coordinator = claims['sub']
            coordinator = CoordinatorModel.find_email_in_tutoring_program(email_coordinator)
            if coordinator:
                return coordinator.json(), 200
            return {'message': 'Coordinator not found'}, 404
        
        # Get the user if the role is student
        if claims['role'] == 'student':
            email_student = claims['sub']
            student = StudentModel.find_email_in_tutoring_program(email_student, tutoring_program_active.cod_tutoring_program)
            if student:
                return student.json(), 200
            return {'message': 'Student not found.'}, 404
        
        # Get the user if the role is principal
        if claims['role'] == 'principal':
            email_principal = claims['sub']
            teacher = TeacherModel.find_email_in_tutoring_program(email_principal, tutoring_program_active.cod_tutoring_program)
            if not teacher:
                return {'message': 'Teacher not found.'}, 404
            principal = PrincipalModel.find_teacher_in_tutoring_program(tutoring_program_active.cod_tutoring_program, teacher.cod_teacher)    
            if principal:
                return principal.json(), 200
            return {'message': "Principal not found."}, 404

        # Get the user if the role is student helper
        if claims['role'] == 'student_helper':
            email_student = claims['sub']            
            student = StudentModel.find_email_in_tutoring_program(email_student, tutoring_program_active.cod_tutoring_program)
            if not student:
                return {"message": "Student not found."}, 404
            student_helper = StudentHelperModel.find_student_in_tutoring_program(tutoring_program_active.cod_tutoring_program, student.cod_student)
            if student_helper :
                return student.json(), 200
            return {"message": "Student Helper not found."}, 404
    