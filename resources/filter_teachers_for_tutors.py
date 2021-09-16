from resources.teacher import TeacherList
from typing import List
from flask_restful import Resource
from flask import request
from models.tutor import TutorModel
from models.tutoring_program import TutoringProgramModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt


class Filter_Tutors_from_Teachers(Resource):
    
    # parser = Req_Parser()    
    # parser.add_argument('tutors_list', list, True)
    
    @jwt_required()
    def put(self):
        claims = get_jwt()
        if not claims['role'] == 'principal':
            return {'message': 'You are not allow to do this'}, 404
        # Return a teacher if found in database
        # ans, data = Filter_Tutors_from_Teachers.parser.parse_args(dict(request.json))
        # if not ans:
        #     return data

        data = dict(request.json)
        print("=======================================================================")
        print(data)
        # Get tutoring program
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()

        for teacher in data['tutors_list']:
            tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher['cod_teacher'])
            if not tutor:
                tutor  = TutorModel(self.create_cod_tutor(), teacher['cod_teacher'], tutoring_program.cod_tutoring_program, '', '')
                try:
                    tutor.save_to_db()
                except:
                    return {'message': 'An error ocurred while trying add Tutor in DB'} , 500
        tutor_list = [ tutor.json() for tutor in TutorModel.find_all() ]
        tutor_list = sorted(tutor_list, key=lambda x: x[list(tutor_list[0].keys())[0]])
    
        return tutor_list, 200

    def create_cod_tutor(self):
        list_tutors = TutorModel.find_all()
        list_tutors = [ tutor.json() for tutor in list_tutors]
        list_tutors = sorted(list_tutors, key=lambda x: x[list(list_tutors[0].keys())[0]])
        if len(list_tutors) == 0 :
            return 'TU-001'
        max = list_tutors[-1]['cod_tutor']
        max = str(max)
        entero=int(max[-3:])
        new_code = max[:3] + '{:>03}'.format(str(entero+1))
        return new_code
