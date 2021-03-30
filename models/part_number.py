from db import db


class PartNumberModel(db.Model):
    __tablename__ = 'part_numbers'

    part_number = db.Column(db.String(100), primary_key=True)

    catalogue = db.relationship('CatalogueModel')
    product = db.relationship('ProductModel')

    def __init__(self, part_number):
        self.part_number = part_number

    def json(self):
        return {'part_number': self.part_number}

    @classmethod
    def find_by_part_number(cls, part_number):
        return cls.query.filter_by(part_number=part_number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
