from db import db

class StudentHelperModel(db.Model):
    __tablename__ = 'student_helpers'
    
    cod_student_helper = db.Column(db.String(6), primary_key=True)
    cod_student = db.Column(db.String(6), db.ForeignKey('students.cod_student'), primary_key=True)
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)

    # -- Relations --
    student_helpers_tutor = db.relationship('StudentHelperTutorModel')
    workshop = db.relationship('WorkshopModel')

    def __init__(self, cod_student_helper, cod_student, cod_tutoring_program):
        self.cod_student_helper = cod_student_helper
        self.cod_student = cod_student
        self.cod_tutoring_program = cod_tutoring_program

    def json(self):
        return {'cod_student_helper' : self.cod_student_helper,
                'cod_student': self.cod_student,
                'cod_tutoring_program' : self.cod_tutoring_program
                }

    def update_data(self, cod_student_helper, cod_student, cod_tutoring_program):
        self.cod_student_helper = cod_student_helper
        self.cod_student = cod_student
        self.cod_tutoring_program = cod_tutoring_program

    @classmethod
    def find_by_cod_student_helper(cls, _cod_student_helper):
        # -> SELECT * FROM items where cod_student_helper=cod_student_helper LIMIT 1
        return cls.query.filter_by(cod_student_helper=_cod_student_helper).first()

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