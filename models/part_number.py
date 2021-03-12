from db import db

class PartNumberModel(db.Model):
  __tablename__ = 'part_numbers'
  
  id = db.Column(db.Integer, primary_key=True)  
  num_part = db.Column(db.String(90), unique=True, nullable=False)

  catalogue = db.relationship('CatalogueModel')
  product = db.relationship('ProductModel')

  def __init__(self, num_part):    
    self.num_part = num_part    

  def json(self):
    return {'id': self.id,
            'num_part': self.num_part}

  @classmethod
  def find_by_num_part(cls, num_part):
    return cls.query.filter_by(num_part=num_part).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      