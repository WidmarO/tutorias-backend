from db import db


class TutorStudentModel(db.Model):
    __tablename__ = 'tutor_students'
    
    cod_tutor = db.Column(db.String(6), db.ForeignKey('tutors.cod_tutor'), primary_key=True)
    cod_student = db.Column(db.String(6), db.ForeignKey('students.cod_student'), primary_key=True)
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)


    #relation
    
    #cod_coordinator = db.relationship('Tutoring_ProgramModel')

    def _init_(self, cod_tutor, cod_tutoring_program,cod_student):
        self.cod_tutor = cod_tutor
        self.cod_tutoring_program= cod_tutoring_program
        self.cod_student= cod_student



    def json(self):
        return {'cod_tutor': self.cod_tutor,
                'cod_tutoring_program': self.cod_tutoring_program,
                'cod_student': self.cod_student,
                }

    def update_data(self,cod_tutor, cod_tutoring_program,cod_student):
        self.cod_tutor = cod_tutor
        self.cod_tutoring_program= cod_tutoring_program
        self.cod_student= cod_student


    @classmethod
    def find_by_cod_tutor(cls, _cod_tutor):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_tutor=_cod_tutor).first()
    
    @classmethod
    def find_by_cod_tutoring_program(cls, _cod_tutoring_program):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program).first()
            
    @classmethod
    def find_by_cod_student(cls, _cod_student):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_student=_cod_student).first()

    @classmethod
    def find_equal_value(cls, _cod_tutor, _cod_student):
        return cls.query.filter_by(cod_tutor=_cod_tutor).filter_by(cod_student=_cod_student).first()

    
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