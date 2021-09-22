from resources.documentation import Documentation
from threading import ExceptHookArgs
from models.tutoring_program import TutoringProgramModel
from flask_restful import Resource
from flask import request
from models.student import StudentModel
from models.tutor import TutorModel
from models.teacher import TeacherModel
from models.tutor_student import TutorStudentModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

class DistributeStudent(Resource):
    parser = Req_Parser()    
    parser.add_argument('tutor_student_list', list, True)

    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
    
        #==============================================================================
        # Go athrough the list of tutors and for each tutor, go through his list of students.                
                # verify for each student if student is in S
                # if the student is in S, add the student to the new tutors_students_list  in the tutor position (use a dictionary)
                # and pop the student of the list of students S

                # Get the max number of students per tutor, going athrougt the NTS and get the max number of students per tutor

                # while there are students in S
                    # Go athrougt the list of tutors and verify if the number of students is less than 
                    # the max number of students per tutor
                        # if the number of students is less than the max number of students per tutor,
                            # from the rest of students list, add one student to the tutor in the new_tutors_students_list 
                            # and pop the student of the list of students S

        # =============================================================================
        # Get the before code of the tutoring program     
        current_tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        current_code_tutoring_program = current_tutoring_program.cod_tutoring_program
        before_code_tutoring_program = current_code_tutoring_program.split('-')[1] # '002'
        before_code_tutoring_program = int(before_code_tutoring_program) 
        if before_code_tutoring_program > 1:
            before_code_tutoring_program = before_code_tutoring_program - 1   
            before_code_tutoring_program = 'PT-' + '{:>03}'.format(str(before_code_tutoring_program))
            # Get the before distribution of students by tutors BTS (before tutors students list)
            before_tutor_students_list =  [ tutor_student.json() for tutor_student in TutorStudentModel.find_by_cod_tutoring_program(before_code_tutoring_program)]
            # Sorted the before_tutor_students_list
            sorted_before_tsl = sorted(before_tutor_students_list, key=lambda x: x[list(before_tutor_students_list[0].keys())[0]])
            # { cod_tutor, cod_student, cod_tutoring_program }

            # get data of sorted_before_tsl into an dictionary
            before_tutor_students_list = {}
            for t in sorted_before_tsl:
                before_tutor_students_list[t['cod_tutor']] = []
            for d in sorted_before_tsl:
                before_tutor_students_list[d['cod_tutor']].append(d['cod_student'])

            # Get the current list of students sorted S
            current_students_list = [ student.cod_student for student in StudentModel.find_by_cod_tutoring_program(current_code_tutoring_program)]

            # Get the current list of tutors sorted T
            current_tutors_list = [ tutor.cod_tutor for tutor in TutorModel.find_by_cod_tutoring_program(current_code_tutoring_program)]

            # Define the new_tutors_students_list NTS (empty)
            new_tutor_students_list = {}
            for t in current_tutors_list:
                new_tutor_students_list[t] = []

            # Go athrough the list of tutors and for each tutor, go through his list of students.
            # For each Tutor in NTS:
                # For each Student in NTS[tutor]:
                    # If the student is in the list of students(S), add it to the list of students of the Tutor
                    # Pop the student from the list of students(S)
            for tutor in before_tutor_students_list:
                for student in before_tutor_students_list[tutor]:
                    if tutor in new_tutor_students_list:
                        if student in current_students_list:
                            new_tutor_students_list[tutor].append(student)
                            current_students_list.remove(student)

            # Get the max number of students per tutor, going athrougt the NTS and get the max number of students per tutor
            max_students_per_tutor = 0
            for tutor in new_tutor_students_list:
                if len(new_tutor_students_list[tutor]) > max_students_per_tutor:
                    max_students_per_tutor = len(new_tutor_students_list[tutor])

            # while there are students in S
                # Go athrougt the list of tutors and verify if the number of students is less than 
                # the max number of students per tutor
                # For each Tutor in NTS:
                    # Get the len of Tutor's students list
                    # if the number of students is less than the max number of students per tutor 
                        # if there is students in S yet,
                            # from the rest of students list, add one student to the tutor in the new_tutors_students_list 
                            # and pop the student of the list of students S
                        # else break the for loop

            current_students_list = current_students_list[::-1]
            while len(current_students_list) > 0:
                for tutor in new_tutor_students_list:
                    if len(new_tutor_students_list[tutor]) < max_students_per_tutor:
                        if len(current_students_list) > 0:
                            new_tutor_students_list[tutor].append(current_students_list.pop())
                        else:
                            break
            
            # get the max number of students per tutor
            max_students_per_tutor = 0
            for tutor in new_tutor_students_list:
                if len(new_tutor_students_list[tutor]) >= max_students_per_tutor:
                    max_students_per_tutor = len(new_tutor_students_list[tutor])
            # get the min number of students per tutor
            min_students_per_tutor = 0
            for tutor in new_tutor_students_list:
                if len(new_tutor_students_list[tutor]) <= min_students_per_tutor:
                    min_students_per_tutor = len(new_tutor_students_list[tutor])
            # IF all tutors have the same number of students,
            # Do the standard distribute with the rest of students
            if max_students_per_tutor == min_students_per_tutor:
                while len(current_students_list)>0:
                    # t is the tutor
                    for t in current_tutors_list:
                        if len(current_students_list) > 0:
                            # st is the student to add
                            st = current_students_list.pop()
                            new_tutor_students_list[t].append(st)

            # In this point of the code we have the new_tutor_students_list 
            # the next step is save the new data in the database
        else:
            # if the current_code_tutoring_program is the first tutoring program,
            # we do the standard distribute
            current_students_list = [ student.cod_student for student in StudentModel.find_by_cod_tutoring_program(current_code_tutoring_program)]
            current_tutors_list = [ tutor.cod_tutor for tutor in TutorModel.find_by_cod_tutoring_program(current_code_tutoring_program)]
            current_tutor_student_list = [tutor_student.json() for tutor_student in TutorStudentModel.find_by_cod_tutoring_program(current_code_tutoring_program) ]
            new_tutor_students_list = {}
            for t in current_tutors_list:
                new_tutor_students_list[t] = []
            while len(current_students_list)>0:
                for t in current_tutors_list:
                    if len(current_students_list) > 0:
                        st = current_students_list.pop()
                        for s in current_tutor_student_list:
                            if s['cod_student'] != st:
                                new_tutor_students_list[t].append(st)
        
        # Save the new data in the database
        for tutor in new_tutor_students_list:
            for student in new_tutor_students_list[tutor]:
                tutor_student = TutorStudentModel(tutor, current_code_tutoring_program, student)
                try:
                    tutor_student.save_to_db()
                    # Escribir en el archivo history el cambio de tutoring program
                    history_file = open(self.history_file, "a")
                    history_file.write("{} {} {} {} {}\n".format(current_code_tutoring_program, tutor, student, "add", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    history_file.close()
                    
                except:
                    print("message : An error occurred inserting data of the student '{}' for the tutor '{}' in the tutoring program with code '{}'".format(student, tutor, current_code_tutoring_program))

        return {"message":"Distribute successful"}, 200

    @jwt_required()
    def post(self):        
        ans, data = DistributeStudent.parser.parse_args(dict(request.json))
        if not ans:
            return data
        
        tutoring_program_active = TutoringProgramModel.find_tutoring_program_active()
        for tutor_student in data['tutor_student_list']:
            tutor_student['tutoring_program'] = tutoring_program_active.code_tutoring_program
            cod_tutor = tutor_student['cod_tutor']
            teacher = TeacherModel.find_teacher_in_tutoring_program(tutoring_program_active.code_tutoring_program, cod_tutor )
            if not teacher:
                return {"message":"The teacher with code '{}' does not exist in the tutoring program active with code '{}'".format(cod_tutor, tutoring_program_active.code_tutoring_program)}, 400
            
            tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program_active.code_tutoring_program, teacher.cod_teacher)
            if not tutor:
                return {"message":"The tutor with code '{}' does not exist in the tutoring program active with code '{}'".format(cod_tutor, tutoring_program_active.code_tutoring_program)}, 400
            
            tutor_student = TutorStudentModel(tutor.cod_tutor, tutoring_program_active.code_tutoring_program, tutor_student['cod_student'])            
            try:
                tutor_student.save_to_db()
            except:
                return {"message":"An error occurred inserting data of the student '{}' for the tutor '{}' in the tutoring program with code '{}'".format(tutor_student.cod_student, tutor_student.cod_tutor, tutoring_program_active.code_tutoring_program)}, 400

            return {"message":"Distribute successful"}, 200


        student = data['student']
        tutor = data['tutor']
        tutor_student = TutorStudentModel(tutor, tutoring_program_active.cod_tutoring_program, student)
        try:
            tutor_student.save_to_db()
        except:
            return {"message":"An error occurred inserting data of the student '{}' for the tutor '{}' in the tutoring program with code '{}'".format(student, tutor, tutoring_program_active.cod_tutoring_program)}, 500
        return {"message":"Tutor student created successfully"}, 201

