from db import db
from datetime import date
from datetime import datetime

class TutoringProgramModel(db.Model):
    __tablename__ = 'tutoring_programs'
    
    # -- Atributes --
    cod_tutoring_program = db.Column(db.String(6), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    initial_date = db.Column(db.Date, nullable= False, default =date.ctime)
    final_date = db.Column(db.Date, nullable= False, default =date.ctime)
    semester = db.Column(db.String(10), nullable=False)
    condition = db.Column(db.String(10), default=False, nullable=False)
    cod_coordinator = db.Column(db.String(6), db.ForeignKey('coordinators.cod_coordinator'))

    # -- Relations --   
    curricular_advancement = db.relationship('CurricularAdvancementModel')
    new = db.relationship('NewModel')
    principal = db.relationship('PrincipalModel')
    appointment = db.relationship('AppointmentModel')
    student_helper_tutor = db.relationship('StudentHelperTutorModel')
    student_helper = db.relationship('StudentHelperModel')
    student = db.relationship('StudentModel')
    teacher = db.relationship('TeacherModel')
    tutor_student = db.relationship('TutorStudentModel')
    tutor = db.relationship('TutorModel')
    workshop_attendance = db.relationship('WorkshopAttendanceModel')
    workshop_student = db.relationship('WorkshopStudentModel')
    workshop = db.relationship('WorkshopModel')

    def __init__(self, cod_tutoring_program, title, initial_date, final_date, semester, condition, cod_coordinator):
        self.cod_tutoring_program = cod_tutoring_program
        self.title = title
        self.initial_date = initial_date
        self.final_date = final_date
        self.semester = semester
        self.condition = condition
        self.cod_coordinator = cod_coordinator

    def json(self):
        return {'cod_tutoring_program' : self.cod_tutoring_program,
                'title' : self.title,
                'initial_date' : str(self.initial_date),
                'final_date' : str(self.final_date),
                'semester' : self.semester,
                'condition' : self.condition,
                'cod_coordinator': self.cod_coordinator
                }

    def update_data(self, cod_tutoring_program, title, initial_date, final_date, semester, condition, cod_coordinator):
        self.cod_tutoring_program = cod_tutoring_program
        self.title = title
        self.initial_date = initial_date
        self.final_date = final_date
        self.semester = semester
        self.condition = condition
        self.cod_coordinator = cod_coordinator

    @classmethod
    def find_by_cod_tutoring_program(cls, _cod_tutoring_program):
        # -> SELECT * FROM items where cod_tutoring_program=cod_tutoring_program LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program).first()

    @classmethod
    def find_tutoring_program_active(cls):
        return cls.query.filter_by(condition='active').first()


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