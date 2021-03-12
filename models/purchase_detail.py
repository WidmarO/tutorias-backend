from db import db
import datetime

class PurchaseDetailModel(db.Model):
  __tablename__ = 'purchase_details'
  
  id_purchase = db.Column(db.Integer, db.ForeignKey('purchases.id'), primary_key=True)
  _id = db.Column(db.Integer, primary_key=True)  
  id_product = db.Column(db.Integer, db.ForeignKey('products.id'))
  quantity = db.Column(db.Integer)
  unit_price = db.Column(db.Float(precision=2))

  def __init__(self, id_purchase, _id, id_product, quantity, unit_price):   
    self.id_purchase = id_purchase
    self._id = _id
    self.id_product = id_product
    self.quantity = quantity
    self.unit_price = unit_price

  def json(self):
    return {'id_purchase': self.id_purchase,
            '_id': self._id,            
            'id_product': self.id_product,
            'quantity': self.quantity,
            'unit_price': self.unit_price
            }

  @classmethod
  def find_by_id(cls, id_purchase, _id):
    return cls.query.filter_by(id_purchase=id_purchase).filter_by(id=_id).first()
  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      