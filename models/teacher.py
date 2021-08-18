from db import db

class TeacherModel(db.Model):
    __tablename__ = 'teacher'
    cod_teacher = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    f_lastname = db.Column(db.String(50), nullable=False)
    m_lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(80), nullable=False)


    #part_Teacher = db.relationship('PartBrandModel')

    def __init__(self, cod_teacher, name, f_lastname, m_lastname, phone, email):
        self.cod_teacher = cod_teacher
        self.name = name 
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email

    def json(self):
        return { 
                'cod_teacher': self.cod_teacher,
                'name': self.name,
                'f_lastname': self.f_lastname,
                'm_lastname': self.m_lastname,
                'phone': self.phone,
                'email': self.email,
                }

    def update_data(self, cod_teacher, name, f_lastname, m_lastname, phone, email):
        self.cod_teacher = cod_teacher
        self.name = name 
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email

    @classmethod
    def find_by_cod_teacher(cls, _cod_Teacher):
        # -> SELECT * FROM items where dni=dni LIMIT 1
        return cls.query.filter_by(cod_teacher=_cod_Teacher).first()

    @classmethod
    def find_by_first_name(cls, _first_name):
        # -> SELECT * FROM items where id=id LIMIT 1
        return cls.query.filter_by(first_name=_first_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
