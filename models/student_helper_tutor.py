from db import db


class StudentHelperTutorModel(db.Model):
    __tablename__ = 'student_helpers_tutors'
    
    # -- Attributes --
    cod_tutor = db.Column(db.String(6), db.ForeignKey('tutors.cod_tutor'), primary_key=True)
    cod_student_helper = db.Column(db.String(6), db.ForeignKey('student_helpers.cod_student_helper'), primary_key=True)
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)

    # -- Relations --

    def __init__(self, cod_tutor, cod_student_helper,cod_tutoring_program):
        self.cod_tutor = cod_tutor
        self.cod_student_helper= cod_student_helper
        self.cod_tutoring_program= cod_tutoring_program



    def json(self):
        return {'cod_tutor': self.cod_tutor,
                'cod_student_helper': self.cod_student_helper,
                'cod_tutoring_program': self.cod_tutoring_program
                }

    def update_data(self,cod_tutor, cod_student_helper,cod_tutoring_program):
        self.cod_tutor = cod_tutor
        self.cod_student_helper= cod_student_helper
        self.cod_tutoring_program= cod_tutoring_program


    @classmethod
    def find_by_cod_tutor(cls, _cod_tutor):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_tutor=_cod_tutor).first()
    
    @classmethod
    def find_by_cod_tutoring_program(cls, _cod_tutoring_program):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program).first()
            
    @classmethod
    def find_by_cod_student_helper(cls, _cod_student_helper):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_student_helper=_cod_student_helper).first()
    
    @classmethod
    def find_all(cls):
        # -> SELECT * FROM items
        return cls.query.all()
    
    @classmethod
    def find_equal_value(cls, _cod_tutor, _cod_student_helper):
        return cls.query.filter_by(cod_tutor=_cod_tutor).filter_by(cod_student_helper=_cod_student_helper).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()