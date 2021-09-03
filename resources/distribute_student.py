from flask_restful import Resource
from flask import request
from models.student import StudentModel
from models.tutor import TutorModel
from models.tutor_student import TutorStudentModel
from Req_Parser import Req_Parser

class DistributeStudent(Resource):

    def get(self):
        sort_students = [ student.json() for student in StudentModel.find_all() ]
        sort_students = sorted(sort_students, key=lambda x: x[list(sort_students[0].keys())[0]])
        liststudents = sort_students[::-1]
        sort_tutors = [ tutor.json() for tutor in TutorModel.find_all() ]
        sort_tutors = sorted(sort_tutors, key=lambda x: x[list(sort_tutors[0].keys())[0]])
        tp=sort_students[0]['cod_tutoring_program']
        sort_students2 = []
        sort_tutors2 = []
        for i in range(len(liststudents)):
            sort_students2.append(liststudents[i]['cod_student'])
        for j in range(len(sort_tutors)):
            sort_tutors2.append(sort_tutors[j]['cod_tutor'])
        dic = {}
        for t in sort_tutors2:
            dic[t] = []
        while len(sort_students2)>0:
            for t in sort_tutors2:
                if len(sort_students2)>0:
                    s = sort_students2.pop()
                    dic[t].append(s)
        
        for t in dic:
            for s in dic[t]:
                tutor_student = TutorStudentModel(t,tp,s)
                tutor_student.save_to_db()
        return {"message":"Distribute successful"}, 200
