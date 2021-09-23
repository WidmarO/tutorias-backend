from models.teacher import TeacherModel
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt

from models.tutoring_program import TutoringProgramModel
from models.student import StudentModel
from models.tutor import TutorModel
from models.coordinator import CoordinatorModel
from models.principal import PrincipalModel
from models.user import UserModel


class UserTutoringProgram(Resource):    # /user_tutoring_program

    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Create a list empty of user in the tutoring program active
        list_user = []    
        
        # Get the tutoring program active
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active()

        # Get the user if the role is coordinator
        email_coordinator = claims['sub']
        coordinator = CoordinatorModel.find_email_in_tutoring_program(email_coordinator)
        if not coordinator:
            return {'message': 'The coordinator with cod_coordinator {} not exist'.format(coordinator.cod_coordinator)}, 400
        user_coordinator = UserModel.find_by_username(coordinator.email)
        if not user_coordinator:
            return{'message': 'The coordinator with username {} not exist'.format(coordinator.email)}, 400
        list_user.append(user_coordinator)

        # Get the user if the role is principal
        principal = PrincipalModel.find_by_cod_tutoring_program(tutoring_program_active.cod_tutoring_program)
        if not principal:
            return {'message': 'The principal with cod_principal {} not exist'.format(principal.cod_principal)}, 400
        user_principal = UserModel.find_by_username(principal.email)
        if not user_principal:
            return {'message': 'The principal with username {} not exist'.format(principal.email)}, 400
        list_user.append(user_principal)
        
        # Get the user if the role is student
        sort_students_in_tutoring_program = [ student.json() for student in StudentModel.find_by_cod_tutoring_program(tutoring_program_active.cod_tutoring_program) ]
        sort_students_in_tutoring_program = sorted(sort_students_in_tutoring_program, key=lambda x: x[list(sort_students_in_tutoring_program[0].keys())[0]]) 
        for student in sort_students_in_tutoring_program:
            user_student = UserModel.find_by_username(student['email'])
            if not user_student:
                return {'message': 'The student with username {} not exist'.format(student['email'])}, 400
            list_user.append(user_student)

        # Get the user if the role is tutor
        sort_tutors_in_tutoring_program = [ tutor.json() for tutor in TutorModel.find_by_cod_tutoring_program(tutoring_program_active.cod_tutoring_program) ]
        sort_tutors_in_tutoring_program = sorted(sort_tutors_in_tutoring_program, key=lambda x: x[list(sort_tutors_in_tutoring_program[0].keys())[0]])  
        for tutor in sort_tutors_in_tutoring_program:
            teacher = TeacherModel.find_teacher_in_tutoring_program(tutoring_program_active.cod_tutoring_program, tutor['cod_teacher'])
            if not teacher:
                return {'message': 'The teacher with username {} not exist'.format(teacher.email)}, 400
            user_tutor = UserModel.find_by_username(teacher.email)
            if not user_tutor:
                return {'message': 'The tutor with username {} not exist'.format(tutor['email'])}, 400
            list_user.append(user_tutor)

        # Sorted list_user 
        
        list_user_tutoring_program = [ user.json() for user in list_user ]
        # list_user_tutoring_program = sorted(list_user, key=lambda x: x[list(list_user_tutoring_program[0].keys())[0]]) 
        return list_user_tutoring_program, 200