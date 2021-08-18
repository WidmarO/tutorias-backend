from db import db

class StudentModel(db.Model):
    __tablename__ = 'students'
    
    cod_student = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    f_lastname = db.Column(db.String(50))
    m_lastname = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(80))
    cod_faculty = db.Column(db.String(10))
    cod_career = db.Column(db.String(100))
    adress = db.Column(db.String(1000))

    def __init__(self, cod_student, name, f_lastname, m_lastname, phone, email, cod_faculty, cod_career, adress):
        self.cod_student = cod_student
        self.name = name
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email
        self.cod_faculty = cod_faculty
        self.cod_career = cod_career
        self.adress = adress

    def json(self):
        return {'cod_student': self.cod_student,
                'name': self.name,
                'f_lastname': self.f_lastname,
                'm_lastname': self.m_lastname,
                'phone': self.phone,
                'email': self.email,
                'cod_faculty': self.cod_faculty,
                'cod_career': self.cod_career,
                'adress': self.adress
                }

    def update_data(self, cod_student, name, f_lastname, m_lastname, phone, email, cod_faculty, cod_career, adress):
        self.cod_student = cod_student
        self.name = name
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email
        self.cod_faculty = cod_faculty
        self.cod_career = cod_career
        self.adress = adress

    @classmethod
    def find_by_cod_student(cls, cod_student):
        # -> SELECT * FROM items where cod_student=cod_student LIMIT 1
        return cls.query.filter_by(cod_student=cod_student).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
