from flask_restful import Resource
from flask import request
from models.tutor import TutorModel
from models.user import UserModel
from models.teacher import TeacherModel
from models.tutoring_program import TutoringProgramModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt

class Create_Tutor_Accounts(Resource):

    parser = Req_Parser()    
    parser.add_argument('tutor_list', list, True)

    @jwt_required()
    def put(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        data = dict(request.json)
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        for tutor in data['tutor_list']:
            teacher = TeacherModel.find_by_cod_teacher(tutor['cod_teacher'])
            if not teacher:
                return {'message': 'Teacher not found in DB'}, 404
            tutor_user = UserModel.find_by_username(teacher.email)
            if not tutor_user:
                tutor_user  = UserModel(teacher.email, self.create_password_tutor, 'tutor')
                try:
                    tutor_user.save_to_db()
                except:
                    return {'message': 'An error ocurred while trying add User in DB'} , 500
        
        tutor_account_list = [ tutor_user.json() for tutor_user in UserModel.find_by_role('tutor')]
        tutor_account_list = sorted(tutor_account_list, key=lambda x: x[list(tutor_account_list[0].keys())[0]])
        
        return tutor_account_list, 200

    def create_password_tutor(self):
        list_tutor_accounts = UserModel.find_by_role('tutor')
        list_tutor_accounts = [ tutor_account.json() for tutor_account in list_tutor_accounts]
        list_tutor_accounts = sorted(list_tutor_accounts, key=lambda x: x[list(list_tutor_accounts[0].keys())[0]])
        if len(list_tutor_accounts) == 0 :
            return 'tutor'
        
        _string = list_tutor_accounts[-1]['username']
        _string = _string.split('@')
        new_password = _string[0]
        return new_password