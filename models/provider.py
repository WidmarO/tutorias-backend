from db import db

class ProviderModel(db.Model):
  __tablename__ = 'providers'
  
  id = db.Column(db.Integer, primary_key=True)
  dni_ruc = db.Column(db.String(25))
  razon = db.Column(db.String(90))
  address = db.Column(db.String(140))  
  phone = db.Column(db.String(25))
  email = db.Column(db.String(80))

  purchase = db.relationship('PurchaseModel')

  def __init__(self, dni_ruc, razon, address, phone, email):
    self.dni_ruc = dni_ruc
    self.razon = razon
    self.address = address  
    self.phone = phone
    self.email = email

  def json(self):
    return {'id': self.id,
            'dni_ruc': self.dni_ruc,
            'razon': self.razon,            
            'address': self.address,            
            'phone': self.phone,
            'email': self.email
            }

  @classmethod
  def find_by_dni_ruc(cls, dni_ruc):
    return cls.query.filter_by(dni_ruc=dni_ruc).first() # -> SELECT * FROM items where dni=dni LIMIT 1

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first() # -> SELECT * FROM items where id=id LIMIT 1

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      