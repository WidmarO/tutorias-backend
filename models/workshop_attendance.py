from db import db
from datetime import datetime


class WorkshopAttendanceModel(db.Model):
    __tablename__ = 'workshop_attendances'
    
    # -- Atributes --
    cod_attendance = db.Column(db.String(6), primary_key=True)
    cod_workshop = db.Column(db.String(6), db.ForeignKey('workshops.cod_workshop'), primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)    

    # -- Relations --
    description_workshop_attendance = db.relationship('DescriptionWorkshopAttendanceModel')

    def __init__(self, cod_attendance, cod_workshop, date_time, cod_tutoring_program):
        self.cod_attendance = cod_attendance
        self.cod_workshop = cod_workshop
        self.date_time = date_time
        self.cod_tutoring_program = cod_tutoring_program

    def json(self):
        return {'cod_attendance':self.cod_attendance,
                'cod_workshop' : self.cod_workshop,
                'date_time': self.date_time,
                'cod_tutoring_program' : self.cod_tutoring_program
                }

    def update_data(self, cod_attendance, cod_workshop, cod_tutoring_program):
        self.cod_attendance = cod_attendance
        self.cod_workshop = cod_workshop
        self.cod_tutoring_program = cod_tutoring_program

    @classmethod
    def find_by_cod_workshop(cls, _cod_workshop):
        # -> SELECT * FROM items where cod_workshop=cod_workshop LIMIT 1
        return cls.query.filter_by(cod_workshop=_cod_workshop).first()

    @classmethod
    def find_by_cod_cod_attendance(cls, _cod_attendance):
        return cls.query.filter_by(cod_attendance=_cod_attendance).first()

    @classmethod
    def find_equal_value(cls, _cod_workshop, _cod_attendance):
        return cls.query.filter_by(cod_workshop=_cod_workshop).filter_by(cod_attendance=_cod_attendance).first()

    @classmethod
    def get_list_cod_workshop(cls, _cod_workshop):
        return cls.query.filter_by(cod_workshop=_cod_workshop)
    
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