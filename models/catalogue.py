from db import db


class CatalogueModel(db.Model):
    __tablename__ = 'catalogues'
    # The _id column has a problem, isn't autoincremnt, so that this proces we are going to do
    # manually from mysql prompt after create de tables the sentence is:
    # ALTER TABLE `catalogues` CHANGE `_id` `_id` INT(11) NOT NULL AUTO_INCREMENT;
    id = db.Column(db.Integer, unique=True, nullable=False)

    model = db.Column(db.String(100), db.ForeignKey(
        'models.model'), primary_key=True)
    brand = db.Column(db.String(100), db.ForeignKey(
        'brands.brand'), primary_key=True)
    part_number = db.Column(db.String(100), db.ForeignKey(
        'part_numbers.part_number'), primary_key=True)
    motor = db.Column(db.String(100), db.ForeignKey(
        'motors.motor'), primary_key=True)
    aplication = db.Column(db.String(100), db.ForeignKey(
        'aplications.aplication'), primary_key=True)

    def __init__(self, id, model, brand, part_number, motor, aplication):
        self.id = id
        self.model = model
        self.brand = brand
        self.part_number = part_number
        self.motor = motor
        self.aplication = aplication

    def json(self):
        return {'id': self.id,
                'model': self.model,
                'brand': self.brand,
                'part_number': self.part_number,
                'motor': self.motor,
                'aplication': self.aplication
                }

    def update_data(self, model, brand, part_number, motor, aplication):
        self.model = model
        self.brand = brand
        self.part_number = part_number
        self.motor = motor
        self.aplication = aplication

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
