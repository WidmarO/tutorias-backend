from db import db
import datetime

class ProductModel(db.Model):
  __tablename__ = 'products'
  
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)  
  id_part = db.Column(db.Integer, db.ForeignKey('part_numbers.id'))
  id_category = db.Column(db.Integer, db.ForeignKey('categories.id'))
  purchase_price = db.Column(db.Float(precision=2))
  sale_price = db.Column(db.Float(precision=2))  

  purchase_detail = db.relationship('PurchaseDetailModel')

  def __init__(self, id_part, id_category, purchase_price, sale_price): 
    aux = ProductModel.query.all()
    
    self.id_part = id_part
    self.id_category = id_category
    self.purchase_price = purchase_price
    self.sale_price = sale_pric    

  def json(self):
    return {'id': self.id,
            'id_part': self.id_part,
            'id_category': self.id_category,            
            'purchase_price': self.purchase_price,
            'sale_price': self.sale_price            
            }

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()
  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      