from db import db
import datetime

class PurchaseModel(db.Model):
  __tablename__ = 'purchases'
  
  id = db.Column(db.Integer, primary_key=True)  
  id_provider = db.Column(db.Integer, db.ForeignKey('providers.id'))
  total = db.Column(db.Float(precision=2))
  fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  purchase_detail = db.relationship('PurchaseDetailModel')

  def __init__(self, id_provider, total, fecha):    
    self.id_provider = id_provider
    self.total = total
    self.fecha = fecha    

  def json(self):
    return {'id': self.id,
            'total': self.total,
            'fecha': self.fecha          
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
      