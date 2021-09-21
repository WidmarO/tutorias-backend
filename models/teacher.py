from db import db

class TeacherModel(db.Model):
    __tablename__ = 'teachers'

    # -- Attributes --
    cod_teacher = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    f_lastname = db.Column(db.String(50), nullable=False)
    m_lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), primary_key=True)
    filiation = db.Column(db.String(20))
    category = db.Column(db.String(20))
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)

    # -- Relations --
    principal = db.relationship('PrincipalModel')
    tutor = db.relationship('TutorModel')

    def __init__(self, cod_teacher, name, f_lastname, m_lastname, phone, email, filiation, category, cod_tutoring_program):
        self.cod_teacher = cod_teacher
        self.name = name 
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone  
        self.email = email
        self.filiation = filiation
        self.category = category
        self.cod_tutoring_program = cod_tutoring_program

    def json(self):
        return { 
                'cod_teacher': self.cod_teacher,
                'name': self.name,
                'f_lastname': self.f_lastname,
                'm_lastname': self.m_lastname,
                'phone': self.phone,
                'email': self.email,
                'filiation': self.filiation,
                'category': self.category, 
                'cod_tutoring_program': self.cod_tutoring_program
                }

    def update_data(self, cod_teacher, name, f_lastname, m_lastname, phone, email, filiation, category, cod_tutoring_program):
        self.cod_teacher = cod_teacher
        self.name = name 
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email
        self.filiation = filiation
        self.category = category
        self.cod_tutoring_program = cod_tutoring_program

    def update_data_Tutor(self, cod_teacher, phone, filiation, category):
        self.cod_teacher = cod_teacher
        self.phone = phone
        self.filiation = filiation
        self.category = category

    @classmethod
    def find_by_cod_teacher(cls, _cod_teacher):
        # -> SELECT * FROM items where dni=dni LIMIT 1
        return cls.query.filter_by(cod_teacher=_cod_teacher).first()

    @classmethod
    def find_by_cod_tutoring_program(cls, _cod_tutoring_program):
        # -> SELECT * FROM items where dni=dni LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program)

    @classmethod
    def find_teacher_in_tutoring_program(cls, _cod_tutoring_program, _cod_teacher):
        # -> SELECT * FROM items where cod_tutoring_program=cod_tutoring_program LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program).filter_by(cod_teacher=_cod_teacher).first()

    @classmethod
    def find_teacher_by_email_in_tutoring_program(cls, _email, _cod_tutoring_program):
        # -> SELECT * FROM items where email=email LIMIT 1
        return cls.query.filter_by(email=_email).filter_by(cod_tutoring_program=_cod_tutoring_program).first()

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
