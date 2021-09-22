from datetime import datetime
from flask_restful import Resource
from flask import request
from models.appointment import AppointmentModel
from models.tutoring_program import TutoringProgramModel
from models.teacher import TeacherModel
from models.tutor import TutorModel
from models.student import StudentModel
from Req_Parser import Req_Parser
from datetime import date, datetime
from flask_jwt_extended import jwt_required, get_jwt

class Appointment(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_appointment', str, True)
    # parser.add_argument('cod_tutor', str, True)
    parser.add_argument('cod_student', str, True)
    parser.add_argument('date_time', str, True)
    parser.add_argument('general_description', str, True)
    parser.add_argument('private_description', str, True)
    parser.add_argument('diagnosis', str, True)
    # parser.add_argument('cod_tutoring_program', str, True)

    @jwt_required()
    def put(self, cod_appointment):
        claims = get_jwt()

        if claims['role'] != 'tutor':
            return {'message': 'You are not allowed to do this'}, 401
        # Verify if all attributes are in request and are of correct type
        ans, data = AppointmentList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        email_tutor = claims["sub"]
        # Create tutoring program in relation at tutoring program active.
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        data['cod_tutoring_program'] = tutoring_program.cod_tutoring_program
        
        # Create teacher and Verify if teacher exits in database 
        teacher = TeacherModel.find_email_in_tutoring_program(email_tutor, tutoring_program.cod_tutoring_program)
        if not teacher:
            return {"message": "Teacher not found."}, 404
        tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)
        if not tutor:
            return {"message": "Tutorr not found."}, 404
        # Add student's code to data
        data['cod_tutor'] = tutor.cod_teacher 
        # Create a instance of TutoringProgramModel with the data provided
        appointment = AppointmentModel.find_by_cod_appointment(cod_appointment)
        if appointment:
            try:
                appointment.update_data(**data)
                appointment.save_to_db()
                
            except:
                return {'message': 'An error occurred while updating appointment'}, 500
            return appointment.json(), 200
        return {'message': 'Appointment not found.'}, 404

    @jwt_required()
    def get(self, cod_appointment):
        claims = get_jwt()
        if claims['role'] != 'tutor':
            return {'message': 'You are not allowed to do this'}, 401
        appointment = AppointmentModel.find_by_cod_appointment(cod_appointment)
        if appointment:
            return appointment.json(), 200
        return {'message': 'Appointment not found.'}, 404
    
    @jwt_required()
    def delete(self, cod_appointment):
        claims = get_jwt()
        if claims['role'] != 'tutor':
            return {'message': 'You are not allowed to do this'}, 401

        '''Delete a appointment from database if exist in it'''
        appointment = AppointmentModel.find_by_cod_appointment(cod_appointment)
        if appointment:
            try:
                appointment.delete_from_db()
            except:
                return {'message': 'An error occurred while deleting appointment'}, 500
            return appointment.json(), 200
        return {'message': 'Appointment not found.'}


class AppointmentList(Resource):
    parser = Req_Parser()
    parser.add_argument('date_time', str, True)
    parser.add_argument('general_description', str, True)
    parser.add_argument('private_description', str, True)
    parser.add_argument('diagnosis', str, True)
    # @jwt_required()

    @jwt_required()
    def get(self, cod_student):
        claims = get_jwt()

        if claims['role'] != 'tutor':
            return {'message': 'You are not allowed to do this'}, 401

        emailteacher=claims['sub']
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        teacher = TeacherModel.find_email_in_tutoring_program(emailteacher, tutoring_program.cod_tutoring_program)
        if not teacher:
            return {"message": "Teacher not found."}, 404
        tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)
        if not tutor:
            return {"message": "Tutor not found."}, 404
        student = StudentModel.find_by_cod_student(cod_student)
        if not student:
            return {"message": "Student not found."}, 404

        list_appointment_student = [ appointment_student.json() for appointment_student in AppointmentModel.find_appointment_of_student_in_tutoring_program(student.cod_student, tutor.cod_tutor, tutoring_program.cod_tutoring_program)]
        return list_appointment_student, 200

    @jwt_required()
    def post(self, cod_student):
        claims = get_jwt()

        if claims['role'] != 'tutor':
            return {'message': 'You are not allowed to do this'}, 401
        
        email_teacher=claims['sub']
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        teacher = TeacherModel.find_email_in_tutoring_program(email_teacher, tutoring_program.cod_tutoring_program)
        tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)

        # Verify if all attributes are in request and are of correct type
        ans, data = AppointmentList.parser.parse_args(dict(request.json))
        if not ans:
            return data 

        cod_appointment = self.create_cod_appointment()
        data['cod_appointment'] = cod_appointment
        data['cod_tutor'] = tutor.cod_tutor
        data['cod_student'] = cod_student
        data['cod_tutoring_program'] = tutoring_program.cod_tutoring_program
        # Verify if student already exists in database
        # cod_appointment = data['cod_appointment']
        '''Add or created a new appointment in database if already them not exist'''
        if AppointmentModel.find_by_cod_appointment(cod_appointment):
            return {'message': "A tutoring program with cod_appointment: '{}' already exist".format(cod_appointment)}
        
        # Create a instance of AppointmentModel with the data provided
        appointment = AppointmentModel(**data)
        
        # Try to insert the student in database
        try:
            appointment.save_to_db()
        except:
            return {'message': "An error ocurred adding the appointment"}, 500
        
        # Return the student data with a status code 201
        return appointment.json(), 201

    def create_cod_appointment(self):
        list_appointments = AppointmentModel.find_all()
        list_appointments = [ appointment.json() for appointment in list_appointments]
        list_appointments = sorted(list_appointments, key=lambda x: x[list(list_appointments[0].keys())[0]])
        if len(list_appointments) == 0 :
            return 'CA-001'
        max = list_appointments[-1]['cod_appointment']
        max = str(max)
        entero=int(max[-3:])
        new_code = max[:3] + '{:>03}'.format(str(entero+1))
        return new_code


class AppointmentListTutoringProgram(Resource):   #appointment_list/cod_tutoring_program
    
    @jwt_required()
    def get(self, cod_tutoring_program, cod_student):
        claims = get_jwt()
        if claims['role'] != 'coordinator':
            return {'message': 'You are not allowed to do this'}, 401
        # Return all students in database        
        list_appointments_in_tutoring_program = [ appointment.json() for appointment in AppointmentModel.find_by_cod_tutoring_program(cod_tutoring_program) ]
        list_appointments_in_tutoring_program = sorted(list_appointments_in_tutoring_program, key=lambda x: x[list(list_appointments_in_tutoring_program[0].keys())[0]])    
        return list_appointments_in_tutoring_program, 200

class AppointmentTutor(Resource):   #list_student_appointment/cod_student/cod_tutoring_program

    @jwt_required()
    def get(self, cod_student, cod_tutoring_program):
        claims = get_jwt()
        if claims['role'] != 'tutor':
            return {'message': 'You are not allowed to do this'}, 401

        email_tutor = claims['email']
        teacher = TeacherModel.find_teacher_by_email_in_tutoring_program(email_tutor, cod_tutoring_program)
        if not teacher:
            return {'message': 'The teacher with email {} not exist'.format(email_tutor)}, 400
        tutor = TutorModel.find_teacher_in_tutoring_program(cod_tutoring_program, teacher.cod_teacher)
        if not tutor:
            return {'message': 'The tutor with code {} not exist'.format(teacher.cod_teacher)}, 400

        # Return all students in database        
        list_appointments_of_a_student_in_tp = [ appointment.json() for appointment in AppointmentModel.find_appointment_of_student_in_tutoring_program(cod_student, tutor.cod_tutor, cod_tutoring_program) ]
        list_appointments_of_a_student_in_tp = sorted(list_appointments_of_a_student_in_tp, key=lambda x: x[list(list_appointments_of_a_student_in_tp[0].keys())[0]])    
        return list_appointments_of_a_student_in_tp, 200
