from db import db

class BrandModel(db.Model):
  __tablename__ = 'brands'
  
  id = db.Column(db.Integer, primary_key=True)  
  brand = db.Column(db.String(90), unique=True, nullable=False)

  catalogue = db.relationship('CatalogueModel')

  def __init__(self, brand):    
    self.brand = brand    

  def json(self):
    return {'id': self.id,
            'brand': self.brand}

  @classmethod
  def find_by_brand(cls, brand):
    return cls.query.filter_by(brand=brand).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      