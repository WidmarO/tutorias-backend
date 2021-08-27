from db import db

class CoordinatorModel(db.Model):
    __tablename__ = 'coordinators'
    
    # COO-001
    cod_coordinator = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    f_lastname = db.Column(db.String(40))
    m_lastname = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

    # -- Relations --
    tutoring_program = db.relationship('TutoringProgramModel')    

    def __init__(self, cod_coordinator, name, f_lastname, m_lastname, phone, email):
        self.cod_coordinator = cod_coordinator
        self.name = name
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email


    def json(self):
        return {'cod_coordinator': self.cod_coordinator,
                'name': self.name,
                'f_lastname': self.f_lastname,
                'm_lastname': self.m_lastname,
                'phone': self.phone,
                'email': self.email
                }

    def update_data(self, cod_coordinator, name, f_lastname, m_lastname, phone, email):
        self.cod_coordinator = cod_coordinator
        self.name = name
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email

    @classmethod
    def find_by_cod_coordinator(cls, _cod_coordinator):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_coordinator=_cod_coordinator).first()

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