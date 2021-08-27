from db import db

class WorkshopStudentModel(db.Model):
    __tablename__ = 'workshop_students'
    
    cod_workshop = db.Column(db.String(6), db.ForeignKey('workshops.cod_workshop'), primary_key=True)
    cod_student = db.Column(db.String(6), db.ForeignKey('students.cod_student'), primary_key=True)
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)

    def __init__(self, cod_workshop, cod_student, cod_tutoring_program):
        self.cod_workshop = cod_workshop
        self.cod_student = cod_student
        self.cod_tutoring_program = cod_tutoring_program

    def json(self):
        return {'cod_workshop' : self.cod_workshop,
                'cod_student': self.cod_student,
                'cod_tutoring_program' : self.cod_tutoring_program
                }

    def update_data(self, cod_workshop, cod_student, cod_tutoring_program):
        self.cod_workshop = cod_workshop
        self.cod_student = cod_student
        self.cod_tutoring_program = cod_tutoring_program

    @classmethod
    def find_by_cod_workshop(cls, _cod_workshop):
        # -> SELECT * FROM items where cod_workshop=cod_workshop LIMIT 1
        return cls.query.filter_by(cod_workshop=_cod_workshop).first()

    @classmethod
    def find_by_cod_student(cls, _cod_student):
        return cls.query.filter_by(cod_student=_cod_student).first()

    @classmethod
    def find_equal_value(cls, _cod_workshop, _cod_student):
        return cls.query.filter_by(cod_workshop=_cod_workshop).filter_by(cod_student=_cod_student).first()

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