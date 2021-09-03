from flask_restful import Resource
from flask import request
from models.tutor_student import TutorStudentModel
from Req_Parser import Req_Parser


class TutorStudentT(Resource):
    def get(self, cod_tutor, cod_tutoring_program):
        # Return a teacher if found in database

        sort_tutor_student = [ tutor_student.json() for tutor_student in TutorStudentModel.find_students_by_tutor_in_tutoring_program(cod_tutoring_program, cod_tutor) ]
        return sort_tutor_student, 200


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

        # Verify if all attributes are in request and are of corrects type
        ans, data = TutorStudentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

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

