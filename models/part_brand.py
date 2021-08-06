from db import db


class PartBrandModel(db.Model):
    __tablename__ = 'parts_brands'

    part_number = db.Column(db.String(100), db.ForeignKey(
        'part_numbers.part_number'), primary_key=True)

    brand = db.Column(db.String(100), db.ForeignKey(
        'brands.brand'), primary_key=True)

    def __init__(self, part_number, brand):
        self.part_number = part_number
        self.brand = brand

    def json(self):
        return {'part_number': self.part_number,
                'brand': self.brand}

    @classmethod
    def find_by_part_number(cls, part_number):
        return cls.query.filter_by(part_number=part_number).first()

    @classmethod
    def find_by_brand(cls, brand):
        return cls.query.filter_by(brand=brand).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
