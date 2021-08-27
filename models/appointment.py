from db import db
from datetime import datetime

class AppointmentModel(db.Model):
    __tablename__ = 'appointments'
    # -- Atributes --
    cod_appointment = db.Column(db.String(6), primary_key=True)
    cod_tutor = db.Column(db.String(6), db.ForeignKey('tutors.cod_tutor'), primary_key=True)
    cod_student = db.Column(db.String(6), db.ForeignKey('students.cod_student'), primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    general_description = db.Column(db.String(300))
    private_description = db.Column(db.String(300))
    diagnosis = db.Column(db.String(300))
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)

    # -- Relations --    

    def __init__(self, cod_appointment, cod_tutor, cod_student,date_time,general_description,private_description,diagnosis,cod_tutoring_program):
        self.cod_appointment = cod_appointment
        self.cod_tutor = cod_tutor
        self.cod_student= cod_student
        self.date_time = date_time
        self.general_description= general_description
        self.private_description = private_description
        self.diagnosis= diagnosis
        self.cod_tutoring_program= cod_tutoring_program

    def json(self):
        return {'cod_appointment': self.cod_appointment,
                'cod_tutor': self.cod_tutor,
                'cod_student': self.cod_student,
                'date_time': self.date_time,
                'general_description': self.general_description,
                'private_description': self.private_description,
                'diagnosis': self.diagnosis,
                'cod_tutoring_program': self.cod_tutoring_program,
                }

    def update_data(self,cod_appointment, cod_tutor, cod_student,date_time,general_description,private_description,diagnosis,cod_tutoring_program):
        self.cod_appointment = cod_appointment
        self.cod_tutor = cod_tutor
        self.cod_student= cod_student
        self.date_time = date_time
        self.general_description= general_description
        self.private_description = private_description
        self.diagnosis= diagnosis
        self.cod_tutoring_program= cod_tutoring_program


    @classmethod
    def find_by_cod_appointment(cls, _cod_appointment):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_appointment=_cod_appointment).first()
    
    @classmethod
    def find_all(cls):
        # -> SELECT * FROM items
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()