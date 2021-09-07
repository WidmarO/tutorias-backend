from datetime import datetime
from flask_restful import Resource
from flask import request
from models.appointment import AppointmentModel
from Req_Parser import Req_Parser
from datetime import date, datetime

class Appointment(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_appointment', str, True)
    parser.add_argument('cod_tutor', str, True)
    parser.add_argument('cod_student', str, True)
    parser.add_argument('date_time', str, True)
    parser.add_argument('general_description', str, True)
    parser.add_argument('private_description', str, True)
    parser.add_argument('diagnosis', str, True)
    parser.add_argument('cod_tutoring_program', str, True)
    # @jwt_required()

    def put(self, cod_appointment):
        # Verify if all attributes are in request and are of correct type
        ans, data = AppointmentList.parser.parse_args(dict(request.json))
        if not ans:
            return data
        # Create a instance of TutoringProgramModel with the data provided
        appointment = AppointmentModel.find_by_cod_appointment(cod_appointment)
        if appointment:
            appointment.update_data(**data)
            appointment.save_to_db()
            return appointment.json(), 200
        return {'message': 'Appointment not found.'}, 404

    def get(self, cod_appointment):
        appointment = AppointmentModel.find_by_cod_appointment(cod_appointment)
        if appointment:
            return appointment.json(), 200
        return {'message': 'Appointment not found.'}, 404
    
    def delete(self, cod_appointment):
        '''Delete a appointment from database if exist in it'''
        appointment = AppointmentModel.find_by_cod_appointment(cod_appointment)
        if appointment:
            appointment.delete_from_db()
            return appointment.json(), 200

        return {'message': 'Appointment not found.'}


class AppointmentList(Resource):
    parser = Req_Parser()
    parser.add_argument('cod_appointment', str, True)
    parser.add_argument('cod_tutor', str, True)
    parser.add_argument('cod_student', str, True)
    parser.add_argument('date_time', str, True)
    parser.add_argument('general_description', str, True)
    parser.add_argument('private_description', str, True)
    parser.add_argument('diagnosis', str, True)
    parser.add_argument('cod_tutoring_program', str, True)
    # @jwt_required()

    def get(self):

        # Return all appointments in database
        sort_appointments = [ appointment.json() for appointment in AppointmentModel.find_all()]
        sort_appointments = sorted(sort_appointments, key=lambda x: x[list(sort_appointments[0].keys())[0]])
        print(sort_appointments)
        return sort_appointments
        # return {'message': 'List of Appointments'}


    def post(self):

        # Verify if all attributes are in request and are of correct type
        ans, data = AppointmentList.parser.parse_args(dict(request.json))
        if not ans:
            return data 

        # Verify if student already exists in database
        cod_appointment = data['cod_appointment']
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
