from db import db
from datetime import datetime

class DescriptionWorkshopAttendanceModel(db.Model):
    __tablename__ = 'description_workshop_attendance'
    # -- Atributes --
    cod_student = db.Column(db.String(6), db.ForeignKey('students.cod_student'), primary_key=True)
    attendance = db.Column(db.Boolean, default=False, nullable=False)
    cod_attendance = db.Column(db.String(6), db.ForeignKey('workshop_attendances.cod_attendance'), primary_key=True)    
    
    # -- Relations --  

    def __init__(self, cod_student, attendance, cod_attendance):
        self.cod_student = cod_student
        self.attendance = attendance
        self.cod_attendance = cod_attendance

    def json(self):
        return {'cod_workshop' : self.cod_workshop,
                'cod_student': self.cod_student,
                'cod_tutoring_program' : self.cod_tutoring_program
                }

    def update_data(self, cod_student, attendance, cod_attendance):
        self.cod_student = cod_student
        self.attendance = attendance
        self.cod_attendance = cod_attendance

    @classmethod
    def find_by_cod_attendance(cls, _attendance):
        # -> SELECT * FROM items where attendance=_attendance LIMIT 1
        return cls.query.filter_by(cod_attendance=_attendance).first()

    @classmethod
    def find_by_cod_student(cls, _cod_student):
        return cls.query.filter_by(cod_student=_cod_student).first()

    @classmethod
    def find_equal_value(cls, _cod_attendance, _cod_student):
        return cls.query.filter_by(cod_attendance=_cod_attendance).filter_by(cod_student=_cod_student).first()

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