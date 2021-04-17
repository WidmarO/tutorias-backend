from db import db


class EmployeeModel(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(15))
    name = db.Column(db.String(90))
    f_lastname = db.Column(db.String(50))
    m_lastname = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(15))
    address = db.Column(db.String(140))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(80))

    def __init__(self, dni, name, f_lastname, m_lastname, age, gender, address, phone, email):
        self.dni = dni
        self.name = name
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.age = age
        self.gender = gender
        self.address = address
        self.phone = phone
        self.email = email

    def json(self):
        return {
            'id': self.id,
            'dni': self.dni,
            'name': self.name,
            'f_lastname': self.f_lastname,
            'm_lastname': self.m_lastname,
            'age': self.age,
            'gender': self.gender,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }

    def update_data(self, dni, name, f_lastname, m_lastname, age, gender, address, phone, email):
        self.dni = dni
        self.name = name
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.age = age
        self.gender = gender
        self.address = address
        self.phone = phone
        self.email = email

    @classmethod
    def find_by_dni(cls, dni):
        # -> SELECT * FROM items where dni=dni LIMIT 1
        return cls.query.filter_by(dni=dni).first()

    @classmethod
    def find_by_id(cls, _id):
        # -> SELECT * FROM items where id=id LIMIT 1
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
