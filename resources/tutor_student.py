from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
# from flask_jwt import jwt_required
from models.tutor_student import TutorStudentModel
from Req_Parser import Req_Parser


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
        #print(request.json)
        #cod_tutor = request.json['cod_tutor']

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
    def get(self, cod_tutor):
        # Return a teacher if found in database
        sort_tutor_student = [ tutor_student.json() for tutor_student in TutorStudentModel.find_by_cod_tutor(cod_tutor) ]
        return sort_tutor_student, 200


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

        print(request.json)
        cod_tutor = request.json['cod_tutor']
        '''Add or created a new tutor_student in database if already them not exist'''
        if TutorStudentModel.find_by_cod_tutor(cod_tutor):
            return {'message': "A tutor_student with cod_tutor: '{}' already exist".format(cod_tutor)}
        # Verify if all attributes are in request and are of correct type
        # Verify if all attributes are in request and are of corrects type
        ans, data = TutorStudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Create a instance of TutorStudentModel with the data provided
        tutor_student = TutorStudentModel(**data)

        try:
            tutor_student.save_to_db()
        except:
            return {'message': "An error ocurred adding the tutor_student"}, 500

        return tutor_student.json(), 201
        # Verify if teacher already exists in database
        cod_tutor = data['cod_tutor']
        cod_student = data['cod_student'] 
        cod_tutoring_program=data['cod_tutoring_program']       
        if TutorStudentModel.find_if_relation_exists_in_tutoring_program(cod_tutor,cod_student,cod_tutoring_program):
            return {'message': "A tutor with cod_tutor: '{}' already has a student with that cod_student in this tutoring program".format(cod_tutor)}

        # Create a instance of TutorStudentModel with the data provided
        tutor_student = TutorStudentModel(**data)

        # Try to insert the TutorStudent in database
        try:
            tutor_student.save_to_db()
        except:
            return {'message': "An error ocurred when adding the tutor-student in DB"}, 500

        # Return the student data with a status code 201
        return tutor_student.json(), 201