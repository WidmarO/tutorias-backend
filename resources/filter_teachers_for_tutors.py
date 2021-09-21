from resources.teacher import TeacherList
from typing import List
from flask_restful import Resource
from flask import request
from models.tutor import TutorModel
from models.tutoring_program import TutoringProgramModel
from models.teacher import TeacherModel
from models.user import UserModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt


class Filter_Tutors_from_Teachers(Resource):
    
    parser = Req_Parser()    
    parser.add_argument('tutor_list', list, True)
    # receive:
    # [cod_teacher, name, f_lastname, m_lastname, email, phone]

    @jwt_required()
    def put(self):
        claims = get_jwt()
        if not claims['role'] == 'principal':
            return {'message': 'You are not allow to do this'}, 404

        # verify if the request is valid
        ans, data = Filter_Tutors_from_Teachers.parser.parse_args(dict(request.json))
        if not ans:
            return data
        
        # Get tutoring program
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()

        current_tutors_list = [ dict(tutor.json()) for tutor in TutorModel.find_by_cod_tutoring_program(tutoring_program.cod_tutoring_program) ]
        current_codes_tutors_list = [ tutor['cod_tutor'] for tutor in current_tutors_list ]
        incoming_codes_tutors_list = [ tutor['cod_teacher'] for tutor in data ]
                
        # If already exist in the current table tutor but is not in the incoming list
        # delete the tutor and respective user from the db
        diference_list = []
        for code in current_codes_tutors_list:
            if code not in incoming_codes_tutors_list:
                diference_list.append(code)

        for code in diference_list:
            teacher = TeacherModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, code)
            if not teacher:
                return {'message': "There isn't a teacher with code '{}'".format(teacher.cod_teacher)}, 404
            user = UserModel.find_user_by_username(teacher.email)
            if not user:
                return {'message': "There isn't the user with username '{}' ".format(teacher.email)}, 404
            
            tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, code)
            try:                            
                tutor.delete_from_db()
                user.delete_from_db()
            except:
                print('Error deleting tutor')
                return {'message': 'Error deleting tutor from db'}, 500

        # If the tutor is not in the current table but is in the incoming list        
        for code in incoming_codes_tutors_list:
            if code not in current_codes_tutors_list:
                teacher = TeacherModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, code)
                if teacher:
                    new_tutor = TutorModel(
                        cod_tutor = self.create_cod_tutor(),
                        cod_tutoring_program = tutoring_program.cod_tutoring_program,
                        cod_teacher = code
                    )
                    new_tutor.save_to_db()
                    new_user = UserModel.find_by_username(teacher.email)
                    if new_user:
                        return {'message': 'The teacher with email {} already exist'.format(teacher.email)}, 400
                    else:
                        new_user = UserModel(
                            username = teacher.email,
                            password = self.create_password_tutor(teacher.email),
                            role = 'tutor'
                        )
                        try:
                            new_user.save_to_db()
                        except:
                            return {'message': 'Error creating user'}, 500
                else:
                    return {'message': 'Teacher not found'}, 404

        # si existe pero esta en la lista de nuevos lo actualiza
            else:
                if code in current_codes_tutors_list:
                    teacher = TeacherModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, code)
                    if teacher:
                        tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, code)
                        if tutor:
                            try:
                                tutor.update_data(tutor.cod_tutor, tutoring_program.cod_tutoring_program, tutor.cod_teacher)
                                tutor.save_to_db()
                            except:
                                print('Error updating tutor')


        # tutor_in_tutoring_program = [ tutor.json() for tutor in TutorModel.find_by_cod_tutoring_program(tutoring_program.cod_tutoring_program) ]
        # user_tutor_in_tutoring_program = [ tutor_user.json() for tutor_user in UserModel.find_by_role('tutor')]

        # for t in data['tutor_list']:
        #     teacher = TeacherModel.find_by_cod_teacher(t['cod_teacher'])
        #     if not teacher:
        #         return {'message': 'Teacher not found in DB'}, 404
            
        #     tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)
        #     if not tutor:
        #         tutor  = TutorModel(self.create_cod_tutor(), teacher.cod_teacher, tutoring_program.cod_tutoring_program, '', '')
        #         try:
        #             tutor.save_to_db()
        #         except:
        #             return {'message': 'An error ocurred while trying add Tutor in DB'} , 500    
        #     # tutor_in_tutoring_program.remove(tutor)
            
        #     tutor_user = UserModel.find_by_username(teacher.email)
        #     if not tutor_user:
        #         tutor_user  = UserModel(teacher.email, self.create_password_tutor(teacher.email), 'tutor')
        #         try:
        #             tutor_user.save_to_db()
        #         except:
        #             return {'message': 'An error ocurred while trying add User in DB'} , 500
        #     # user_tutor_in_tutoring_program.remove(tutor_user)

        # for te in tutor_in_tutoring_program:
        #     deletetutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, te['cod_teacher'])
        #     deletetutor.delete_from_db()


        # tutor_account_list = [ tutor_user.json() for tutor_user in UserModel.find_by_role('tutor')]
        # tutor_account_list = sorted(tutor_account_list, key=lambda x: x[list(tutor_account_list[0].keys())[0]])
        tutor_list = [ tutor.json() for tutor in TutorModel.find_by_cod_tutoring_program(tutoring_program.cod_tutoring_program) ]
        tutor_list = sorted(tutor_list, key=lambda x: x[list(tutor_list[0].keys())[0]])

        return tutor_list, 200

    # @jwt_required()
    # def delete(self):
    #     claims = get_jwt()
    #     if not claims['role'] == 'principal':
    #         return {'message': 'You are not allow to do this'}, 404

    #     data = dict(request.json)
    #     # Get tutoring program
    #     tutoring_program = TutoringProgramModel.find_tutoring_program_active()
    #     tutor_list = []
    #     tutor_account_list = []
    #     for t in data['tutor_list']:
    #         teacher = TeacherModel.find_by_cod_teacher(t['cod_teacher'])
    #         if not teacher:
    #             return {'message': 'Teacher not found in DB'}, 404
    #         tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)
    #         if tutor:
    #             tutor.delete_from_db()
    #             tutor_list.append(tutor.json())
    #         else:
    #             return {'message': 'Tutor not found in DB'}, 404           
    #         tutor_user = UserModel.find_by_username(teacher.email)
    #         if tutor_user:
    #             tutor_user.delete_from_db()
    #             tutor_account_list.append(tutor_user.json())
    #         else:
    #             return {'message': 'Tutor User not found in DB'}, 404
    
    #     return tutor_list, 200

    def create_cod_tutor(self):
        list_tutors = TutorModel.find_all()
        list_tutors = [ tutor.json() for tutor in list_tutors]
        list_tutors = sorted(list_tutors, key=lambda x: x[list(list_tutors[0].keys())[0]])
        if len(list_tutors) == 0 :
            return 'TU-001'
        _max = list_tutors[-1]['cod_tutor']
        _max = str(_max)
        entero=int(_max[-3:])
        new_code = _max[:3] + '{:>03}'.format(str(entero+1))
        return new_code

    def create_password_tutor(self, email):
        _string = email.split('@')
        new_password = _string[0]
        return new_password

