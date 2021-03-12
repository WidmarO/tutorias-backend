from db import db

class AplicationModel(db.Model):
  __tablename__ = 'aplications'
  
  id = db.Column(db.Integer, primary_key=True)  
  aplication = db.Column(db.String(90), unique=True, nullable=False)

  catalogue = db.relationship('CatalogueModel')

  
  def __init__(self, aplication):    
    self.aplication = aplication    

  def json(self):
    return {'id': self.id,
            'aplication': self.aplication}

  @classmethod
  def find_by_aplication(cls, aplication):
    return cls.query.filter_by(aplication=aplication).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      