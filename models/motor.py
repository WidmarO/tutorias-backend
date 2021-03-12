from db import db

class MotorModel(db.Model):
  __tablename__ = 'motors'
  
  id = db.Column(db.Integer, primary_key=True)  
  motor = db.Column(db.String(90), unique=True, nullable=False)

  catalogue = db.relationship('CatalogueModel')

  
  def __init__(self, motor):    
    self.motor = motor    

  def json(self):
    return {'id': self.id,
            'motor': self.motor}

  @classmethod
  def find_by_motor(cls, motor):
    return cls.query.filter_by(motor=motor).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      