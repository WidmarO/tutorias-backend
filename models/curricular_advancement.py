from db import db

class CurricularAdvancementModel(db.Model):
    __tablename__ = 'curricular_advancements'
    
    cod_advancement = db.Column(db.String(6), primary_key=True)
    cod_student = db.Column(db.String(6), db.ForeignKey('students.cod_student'))
    advancement = db.Column(db.String(500))
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)
    

    def __init__(self, cod_advancement, cod_student, advancement, cod_tutoring_program):
        self.cod_advancement = cod_advancement
        self.cod_student = cod_student
        self.advancement = advancement
        self.cod_tutoring_program = cod_tutoring_program

    def json(self):
        return {'cod_advancement' : self.cod_advancement,
                'cod_student': self.cod_student,
                'advancement' : self.advancement,
                'cod_tutoring_program' : self.cod_tutoring_program
                }

    def update_data(self, cod_advancement, cod_student, advancement, cod_tutoring_program):
        self.cod_advancement = cod_advancement
        self.cod_student = cod_student
        self.advancement = advancement
        self.cod_tutoring_program = cod_tutoring_program

    @classmethod
    def find_by_cod_advancement(cls, _cod_advancement):
        # -> SELECT * FROM items where cod_advancement=cod_advancement LIMIT 1
        return cls.query.filter_by(cod_advancement=_cod_advancement).first()

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