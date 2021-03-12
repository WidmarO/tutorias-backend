from db import db

class CatalogueModel(db.Model):
  __tablename__ = 'catalogues'
  # The _id column has a problem, isn't autoincremnt, so that this proces we are going to do
  # manually from mysql prompt after create de tables the sentence is:
  # ALTER TABLE `catalogues` CHANGE `_id` `_id` INT(11) NOT NULL AUTO_INCREMENT;
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)  
  id_part = db.Column(db.Integer, db.ForeignKey('part_numbers.id'), primary_key=True)
  id_model = db.Column(db.Integer, db.ForeignKey('models.id'), primary_key=True)
  id_brand = db.Column(db.Integer, db.ForeignKey('brands.id'), primary_key=True)
  id_motor = db.Column(db.Integer, db.ForeignKey('motors.id'), primary_key=True)
  id_aplication = db.Column(db.Integer, db.ForeignKey('aplications.id'), primary_key=True)


  def __init__(self, id_part, id_model, id_brand, id_motor):    
    self.id_part = id_part
    self.id_model = id_model
    self.id_brand = id_brand
    self.id_motor = id_motor

  def json(self):
    return {'_id': self._id,
            'id_part': self.id_part,
            'id_model': self.id_model,
            'id_brand': self.id_brand,
            'id_motor': self.id_motor
            }

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(_id=_id).first()
  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
      