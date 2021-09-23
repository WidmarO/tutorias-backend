from flask_restful import Resource
from flask import request
import bcrypt
from models.principal import PrincipalModel
from models.teacher import TeacherModel
from models.tutoring_program import TutoringProgramModel
from models.user import UserModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt


class Principal(Resource): # /principal/<cod_principal>
    parser = Req_Parser() 
    parser.add_argument('cod_principal', str, True)
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('email', str, True)

    @jwt_required()
    def put(self, cod_principal):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Verify if all arguments are correct
        ans, data = Principal.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Get the tutoring program active 
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active() 
        data['cod_tutoring_program'] = tutoring_program_active.cod_tutoring_program

        # Verify if principal exists in database
        principal = PrincipalModel.find_by_cod_principal(cod_principal)
        if principal:
            principal.update_data(**data)
            try:
                principal.save_to_db()
            except:
                return {'message': 'An error occurred while updating data of the principal.'}, 500
            return principal.json(), 200
        return {'message': 'Director Principal not found.'}, 404

    @jwt_required()
    def get(self, cod_principal):        
        # Return a teacher if found in database
        principal = PrincipalModel.find_by_cod_principal(cod_principal)
        if principal:
            return principal.json(), 200
        return {'message': 'Director Principal not found'}, 404

    @jwt_required()
    def delete(self, cod_principal):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        
        # Delete a principal from database if exist in it
        principal = PrincipalModel.find_by_cod_principal(cod_principal)
        user_principal = UserModel.find_by_username(principal.email)
        if principal and user_principal:
            principal.delete_from_db()
            user_principal.delete_from_db()
            return principal.json(), 202            
        # Return a messagge if not found
        return {'message': 'Director Principal not found.'}, 404


class PrincipalList(Resource): # /principals
    parser = Req_Parser()    
    parser.add_argument('cod_principal', str, True)
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('cod_tutoring_program', str, True)
    
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all teachers in database        
        sort_principal = [ principal.json() for principal in PrincipalModel.find_all() ]
        sort_principal = sorted(sort_principal, key=lambda x: x[list(sort_principal[0].keys())[0]])
        return sort_principal, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()

        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Verify if all attributes are in request and are of corrects type
        ans, data = PrincipalList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if teacher already exists in database
        cod_principal = data['cod_principal']        
        if PrincipalModel.find_by_cod_principal(cod_principal):
            return {'message': "A principal director with cod_principal: '{}' already exist".format(cod_principal)}

        # Create a instance of TeacherModel with the data provided
        principal = PrincipalModel(**data)

        # Try to insert the teacher in database
        try:
            principal.save_to_db()
        except:
            return {'message': "An error ocurred when adding the principal in DB"}, 500

        # Return the teacher data with a status code 201
        return principal.json(), 201

class PrincipalP(Resource):   # /principalP
    parser = Req_Parser()    
    parser.add_argument('phone')
    parser.add_argument('filiation', str, True)
    parser.add_argument('category', str, True)

    @jwt_required()
    def put(self):

        claims = get_jwt()
        if claims['role'] != 'principal':
            return {'message': 'You are not allowed to do this'}, 401

        # Verify if all arguments are correct
        ans, data = PrincipalP.parser.parse_args(dict(request.json))
        if not ans:
            return data

        email_principal = claims["sub"]
        # Create tutoring program in relation at tutoring program active.
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        principal = PrincipalModel.find_email(email_principal,tutoring_program.cod_tutoring_program)
        if not principal:
            return {"message": "Principal not found."}, 404
        # Create teacher and Verify if teacher exits in database 
        teacher = TeacherModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, principal.cod_teacher)
        if not teacher:
            return {"message": "Teacher not found."}, 404

        # Add student's code to data
        data['cod_teacher'] = teacher.cod_teacher 
        print(data)
        # Verify if tutor exists in database
        try:
            teacher.update_data_Principal(**data)
            teacher.save_to_db()
        except:
            return {'message': 'An error occurred while updating the principal.'}, 500
        return teacher.json(), 200


class PrincipalC(Resource): # /principal
    parser = Req_Parser()    
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    parser.add_argument('filiation')
    parser.add_argument('category')

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Verify if all attributes are in request and are of corrects type
        ans, data = PrincipalC.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if teacher already exists in database
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        cod_teacher = data['cod_teacher']
        teacher = TeacherModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, cod_teacher)
        if teacher:
            # Verify if principal already exists in database
            cod_principal = self.create_cod_principal()
            if PrincipalModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher):
                return {'message': "A principal director with cod_teacher: '{}' already exist".format(teacher.cod_teacher)}
            if PrincipalModel.find_by_cod_principal(cod_principal):
                return {'message': "A principal director with cod_principal: '{}' already exist".format(cod_principal)}

            principal = PrincipalModel(cod_principal, teacher.cod_teacher, tutoring_program.cod_tutoring_program, self.create_email_principal(teacher.email))
            # Try to insert the teacher in database
            try:
                principal.save_to_db()
            except:
                return {'message': "An error ocurred when adding the principal in DB"}, 500

            # Create user for principal
            user_principal = UserModel.find_by_username(principal.email)
            if not user_principal:
                password_principal = self.create_password_principal(principal.email)
                hashed_principal = bcrypt.hashpw(password_principal.encode('utf-8'), bcrypt.gensalt())
                user_principal = UserModel(principal.email, hashed_principal, 'principal')
                try:
                    user_principal.save_to_db()
                except:
                    return {'message': "An error ocurred when adding the user principal in DB"}, 500            
            else:
                return {'message': "A principal with username: '{}' already exist".format(principal.email)}
            # Return the teacher data with a status code 201
            return principal.json(), 201

        else: 
            data['cod_tutoring_program'] = tutoring_program.cod_tutoring_program
            teacher = TeacherModel(**data)
            teacher.save_to_db()

            # Verify if principal already exists in database
            cod_principal = self.create_cod_principal()
            if PrincipalModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher):
                return {'message': "A principal director with cod_teacher: '{}' already exist".format(teacher.cod_teacher)}
            if PrincipalModel.find_by_cod_principal(cod_principal):
                return {'message': "A principal director with cod_principal: '{}' already exist".format(cod_principal)}
            
            # Create a instance of PrincipalModel with the data provided
            principal = PrincipalModel(cod_principal, teacher.cod_teacher, tutoring_program.cod_tutoring_program, self.create_email_principal(teacher.email))
            # Try to insert the teacher in database
            try:
                principal.save_to_db()                
            except:
                return {'message': "An error ocurred when adding the principal in DB"}, 500

            user_principal = UserModel.find_by_username(principal.email)
            if not user_principal:
                password_principal = self.create_password_principal(principal.email)
                hashed_principal = bcrypt.hashpw(password_principal.encode('utf-8'), bcrypt.gensalt())
                user_principal = UserModel(principal.email, hashed_principal, 'principal')
                try:
                    user_principal.save_to_db()
                except:
                    return {'message': "An error ocurred when adding the user principal in DB"}, 500
            
            else:
                return {'message': "A principal with username: '{}' already exist".format(principal.email)}
            # Return the teacher data with a status code 201
            return principal.json(), 201

    def create_cod_principal(self):
        list_principals = PrincipalModel.find_all()
        list_principals = [ principal.json() for principal in list_principals]
        list_principals = sorted(list_principals, key=lambda x: x[list(list_principals[0].keys())[0]])
        if len(list_principals) == 0 :
            return 'PR-001'
        _max = list_principals[-1]['cod_principal']
        _max = str(_max)
        entero=int(_max[-3:])
        new_code = _max[:3] + '{:>03}'.format(str(entero+1))
        return new_code

    def create_email_principal(self, email):
        _string = str(email)
        _string = 'D_' + _string 
        new_email = _string
        return new_email

    def create_password_principal(self, email):
        _string = email
        _string = _string.split('@')
        new_password = _string[0]
        return new_password

    