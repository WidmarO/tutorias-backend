from models.tutor import TutorModel
from flask_restful import Resource
from flask import request
from models.teacher import TeacherModel
from models.tutoring_program import TutoringProgramModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt


class Teacher(Resource): # /teacher/<cod_teacher>
    parser = Req_Parser()    
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    parser.add_argument('filiation', str, True)
    parser.add_argument('category', str, True)    

    @jwt_required()
    def put(self, cod_teacher):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Verify if all arguments are correct
        ans, data = TeacherList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Get the tutoring program active 
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active() 
        data['cod_tutoring_program'] = tutoring_program_active.cod_tutoring_program

        # Verify if teacher exists in database
        teacher = TeacherModel.find_by_cod_teacher(cod_teacher)
        if teacher:
            try:
                teacher.update_data(**data)
                teacher.save_to_db()            
                return teacher.json(), 200
            except:
                return {'message': 'An error occurred while updating the teacher on DB'}, 500
        return {'message': 'Teacher not found.'}, 404

    @jwt_required()
    def get(self, cod_teacher):
        # Return a teacher if found in database
        teacher = TeacherModel.find_by_cod_teacher(cod_teacher)
        if teacher:
            return teacher.json(), 200
        return {'message': 'Teacher not found'}, 404

    @jwt_required()
    def delete(self, cod_teacher):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Delete a teacher from database if exist in it
        teacher = TeacherModel.find_by_cod_teacher(cod_teacher)
        if teacher:
            try:
                teacher.delete_from_db()
                return teacher.json(), 200
            except:
                return {'message': 'An error occurred while deleting the teacher from DB'}, 500
        # Return a messagge if not found
        return {'message': 'Teacher not found.'}, 404

class TeacherList(Resource): # /teachers
    parser = Req_Parser()
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('name', str, True)
    parser.add_argument('f_lastname', str, True)
    parser.add_argument('m_lastname', str, True)
    parser.add_argument('phone')
    parser.add_argument('email', str, True)
    parser.add_argument('filiation', str, True)
    parser.add_argument('category', str, True)    
    
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator' and claims['role'] != 'principal':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all teachers in database
        sort_teachers = [ teacher.json() for teacher in TeacherModel.find_all() ]
        sort_teachers = sorted(sort_teachers, key=lambda x: x[list(sort_teachers[0].keys())[0]])
        return sort_teachers, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401

        # Verify if all attributes are in request and are of corrects type
        ans, data = TeacherList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if teacher already exists in database
        cod_teacher = data['cod_teacher']
        if TeacherModel.find_by_cod_teacher(cod_teacher):
            return {'message': "A teacher with cod_teacher: '{}' already exist".format(cod_teacher)}

        # Get the tutoring program active 
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active() 
        data['cod_tutoring_program'] = tutoring_program_active.cod_tutoring_program      

        # Create a instance of TeacherModel with the data provided
        teacher = TeacherModel(**data)

        # Try to insert the teacher in database
        try:
            teacher.save_to_db()
        except:
            return {'message': "An error ocurred when adding the teacher in DB"}, 500

        # Return the teacher data with a status code 201
        return teacher.json(), 201

class TeacherListTutoringProgram(Resource): # /teacher_list/<cod_tutoring_program>
    @jwt_required()
    def get(self, cod_tutoring_program):
        claims = get_jwt()
        if claims['role'] != 'coordinator' and claims['role'] != 'principal':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all teachers of the tutoring program con cod_tutoring_program of the database        
        sort_teachers_in_tutoring_program = [ teacher.json() for teacher in TeacherModel.find_by_cod_tutoring_program(cod_tutoring_program) ]
        sort_teachers_in_tutoring_program = sorted(sort_teachers_in_tutoring_program, key=lambda x: x[list(sort_teachers_in_tutoring_program[0].keys())[0]])    
        return sort_teachers_in_tutoring_program, 200

class AddTeachers(Resource): # /add_teachers

    parser = Req_Parser()    
    parser.add_argument('teacher_list', list, True)
    # receive for each teacher: 
    # [{'cod_teacher': '', 'name': '', 'f_lastname': '', 'm_lastname': '', 'email': ''}]
    
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        
        # Verify if all attributes are in request and are of corrects type
        ans, data = AddTeachers.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # data = dict(request.json)

        tutoring_program = TutoringProgramModel.find_tutoring_program_active()

        count_teachers = 0
        count_teachers_added = 0
        count_teachers_not_added = 0
        for t in data['teacher_list']:
            teacher = TeacherModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program , t['cod_teacher'])
            count_teachers += 1
            t['phone'] = ''
            t['filiation'] = ''
            t['category'] = ''
            if not teacher:
                teacher = TeacherModel(t['cod_teacher'], t['name'], t['f_lastname'], t['m_lastname'], t['phone'], t['email'], t['filiation'], t['category'], tutoring_program.cod_tutoring_program)
                try:
                    teacher.save_to_db()
                except:
                    return {'message': 'An error ocurred while trying add Teacher in DB'} , 500
                count_teachers_added += 1
            else:
                count_teachers_not_added += 1
        
        # teacher_list = [ teacher.json() for teacher in TeacherModel.find_by_cod_tutoring_program(tutoring_program.cod_tutoring_program)]
        # teacher_list = sorted(teacher_list, key=lambda x: x[list(teacher_list[0].keys())[0]])

        return {'message': '{} total_teachers, {} teachers added, {} teachers not added'.format(count_teachers, count_teachers_added, count_teachers_not_added)}, 200


class TeacherListPrincipal(Resource): # /teacher_list_principal
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] != 'principal':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all teachers of the tutoring program con cod_tutoring_program of the database    
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active()    
        sort_teachers_in_tutoring_program = [ teacher.json() for teacher in TeacherModel.find_by_cod_tutoring_program(tutoring_program_active.cod_tutoring_program) ]
        sort_teachers_in_tutoring_program = sorted(sort_teachers_in_tutoring_program, key=lambda x: x[list(sort_teachers_in_tutoring_program[0].keys())[0]]) 
        for teacher in sort_teachers_in_tutoring_program:
            if TutorModel.find_teacher_in_tutoring_program(teacher.cod_teacher):
                teacher['Is_tutor'] = True
            else:
                teacher['Is_tutor'] = False   
        return sort_teachers_in_tutoring_program, 200

