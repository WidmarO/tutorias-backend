from db import db

class PrincipalModel(db.Model):
    __tablename__ = 'principals'
    
    # -- Attributes --
    cod_principal = db.Column(db.String(6), primary_key=True)
    cod_teacher = db.Column(db.String(6), db.ForeignKey('teachers.cod_teacher'), primary_key=True)
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)
    email = db.Column(db.String(100), primary_key=True)

    # -- Relations --
    
    def __init__(self, cod_principal, cod_teacher, cod_tutoring_program, email):
        self.cod_principal = cod_principal
        self.cod_teacher = cod_teacher
        self.cod_tutoring_program = cod_tutoring_program
        self.email = email

    def json(self):
        return {'cod_principal': self.cod_principal,
                'cod_teacher': self.cod_teacher,
                'cod_tutoring_program': self.cod_tutoring_program,
                'email': self.email
                }

    def update_data(self, cod_principal, cod_teacher, cod_tutoring_program, email):
        self.cod_principal = cod_principal
        self.cod_teacher = cod_teacher
        self.cod_tutoring_program = cod_tutoring_program
        self.email = email

    @classmethod
    def find_by_cod_principal(cls, _cod_principal):
        # -> SELECT * FROM items where cod_principal=_cod_principal LIMIT 1
        return cls.query.filter_by(cod_principal=_cod_principal).first()
    
    @classmethod
    def find_by_cod_teacher(cls, _cod_teacher):
        # -> SELECT * FROM items where dni=dni LIMIT 1
        return cls.query.filter_by(cod_teacher=_cod_teacher).first()

    @classmethod
    def find_all(cls):
        # -> SELECT * FROM items
        return cls.query.all()

    @classmethod
    def find_email(cls, _email, _cod_tutoring_program):
        # -> SELECT * FROM items where email=email LIMIT 1
        return cls.query.filter_by(email=_email).filter_by(cod_tutoring_program=_cod_tutoring_program).first()

    @classmethod
    def find_teacher_in_tutoring_program(cls, _cod_tutoring_program, _cod_teacher):
        # -> SELECT * FROM items where cod_tutoring_program=cod_tutoring_program LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program).filter_by(cod_teacher=_cod_teacher).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()