from db import db

class ClientModel(db.Model):
  __tablename__ = 'clients'
  
  id = db.Column(db.Integer, primary_key=True)
  dni = db.Column(db.String(15))
  name = db.Column(db.String(90))
  f_lastname = db.Column(db.String(50))
  m_lastname = db.Column(db.String(50))
  phone = db.Column(db.String(20))
  email = db.Column(db.String(80))

  def __init__(self, dni, name, f_lastname, m_lastname, phone, email):
    self.dni = dni
    self.name = name
    self.f_lastname = f_lastname
    self.m_lastname = m_lastname
    self.phone = phone
    self.email = email

  def json(self):
    return {'dni': self.dni,
            'name': self.name,            
            'f_lastname': self.f_lastname,
            'm_lastname': self.m_lastname,
            'phone': self.phone,
            'email': self.email
            }

  def update_data(self, dni, name, f_lastname, m_lastname, phone, email):
    self.dni = dni
    self.name = name
    self.f_lastname = f_lastname
    self.m_lastname = m_lastname
    self.phone = phone
    self.email = email

  @classmethod
  def find_by_dni(cls, dni):
    return cls.query.filter_by(dni=dni).first() # -> SELECT * FROM items where dni=dni LIMIT 1

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first() # -> SELECT * FROM items where id=id LIMIT 1

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      