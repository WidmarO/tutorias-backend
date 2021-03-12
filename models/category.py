from db import db

class CategoryModel(db.Model):
  __tablename__ = 'categories'
  
  id = db.Column(db.Integer, primary_key=True)  
  category = db.Column(db.String(90), unique=True, nullable=False)

  product = db.relationship('ProductModel')
  
  def __init__(self, category):    
    self.category = category
    
  def json(self):
    return {'category': self.category}

  @classmethod
  def find_by_category(cls, category):
    return cls.query.filter_by(category=category).first()

  @classmethod
  def find_by_id(cls, id):
    return cls.query.filter_by(id=_id).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      