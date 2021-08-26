from db import db
from datetime import datetime

class Tutoring_ProgramModel(db.Model):
    __tablename__ = 'tutoring_programs'
    
    cod_tutoring_program = db.Column(db.String(6), primary_key=True, unique = True)
    title = db.Column(db.String(100), nullable=False)
    inicial_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    final_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    semester = db.Column(db.String(10), nullable=False)
    condition = db.Column(db.Boolean, default=False, nullable=False)
    cod_coordinator = db.Column(db.String(6), db.ForeignKey('coordinators.cod_coordinator'))

    #relation
    student = db.relationship('StudentModel')
    tutors = db.relationship('TutorsModel')
    teacher = db.relationship('TeacherModel')
    principals = db.relationship('PrincipalsModel')
    student_helper_tutors = db.relationship('Student_Helper_TutorsModel')
    student_helpers = db.relationship('Student_HelperModel')
    tutor_students = db.relationship('Tutor_StudentsModel')
                   
    #student_helper = db.relatioship('Student_HelperModel')
    #student_helper = db.relatioship('Student_HelperModel')
    #student_helper = db.relatioship('Student_HelperModel')
    #student_helper = db.relatioship('Student_HelperModel')

    #curricular_advancement = db.relatioship('Curricular_AdvancementModel')
    #workshop_student = db.relatioship('Workshop_StudentModel')

    def __init__(self, cod_tutoring_program, title, inicial_date, final_date, semester, condition, cod_coordinator):
        self.cod_tutoring_program = cod_tutoring_program
        self.title = title
        self.inicial_date = inicial_date
        self.final_date = final_date
        self.semester = semester
        self.condition = condition
        self.cod_coordinator = cod_coordinator

    def json(self):
        return {'cod_tutoring_program' : self.cod_tutoring_program,
                'title' : self.title,
                'inicial_date' : self.inicial_date,
                'final_date' : self.final_date,
                'semester' : self.semester,
                'condition' : self.condition,
                'cod_coordinator': self.cod_coordinator
                }

    def update_data(self, cod_tutoring_program, title, inicial_date, final_date, semester, condition, cod_coordinator):
        self.cod_tutoring_program = cod_tutoring_program
        self.title = title
        self.inicial_date = inicial_date
        self.final_date = final_date
        self.semester = semester
        self.condition = condition
        self.cod_coordinator = cod_coordinator

    @classmethod
    def find_by_cod_tutoring_program(cls, _cod_tutoring_program):
        # -> SELECT * FROM items where cod_tutoring_program=cod_tutoring_program LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program).first()

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