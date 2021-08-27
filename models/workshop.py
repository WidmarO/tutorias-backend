from db import db


class WorkshopModel(db.Model):
    __tablename__ = 'workshops'

    # -- Atributes --
    cod_workshop = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(120), nullable=False) 
    cod_student_helper = db.Column(db.String(6), db.ForeignKey('student_helpers.cod_student_helper'), primary_key=True)     
    classroom = db.Column(db.String(50))
    shedule = db.Column(db.String(20))
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)

    # -- Relations --
    workshop_student = db.relationship('WorkshopStudentModel')
    workshop_attendance = db.relationship('WorkshopAttendanceModel')

    def __init__(self, cod_workshop, name, cod_student_helper, classroom, shedule, cod_tutoring_program):
        self.cod_workshop = cod_workshop
        self.name = name
        self.cod_student_helper = cod_student_helper
        self.classroom = classroom
        self.shedule = shedule
        self.cod_tutoring_program = cod_tutoring_program        

    def json(self):
        return {'cod_workshop': self.cod_workshop,
                'name': self.name,
                'cod_student_helper': self.cod_student_helper,
                'classroom': self.classroom,
                'shedule': self.shedule,
                'cod_tutoring_program': self.cod_tutoring_program                
                }

    def update_data(self, cod_workshop, name, cod_student_helper, classroom, shedule, cod_tutoring_program):
        self.cod_workshop = cod_workshop
        self.name = name
        self.cod_student_helper = cod_student_helper
        self.classroom = classroom
        self.shedule = shedule
        self.cod_tutoring_program = cod_tutoring_program        

    @classmethod
    def find_by_cod_workshop(cls, _cod_workshop):
        # -> SELECT * FROM items where dni=dni LIMIT 1
        return cls.query.filter_by(cod_workshop=_cod_workshop).first()

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
