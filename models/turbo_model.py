from db import db

class TurboModel_Model(db.Model):
  __tablename__ = 'models'
  
  id = db.Column(db.Integer, primary_key=True)
  model = db.Column(db.String(90), unique=True, nullable=False)

  catalogue = db.relationship('CatalogueModel')
  
  def __init__(self, model):
    self.model = model
    
  def json(self):
    return {'id': self.id,
            'model': self.model}

  @classmethod
  def find_by_model(cls, model):
    return cls.query.filter_by(model=model).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      