from db import db


class PartAplicationModel(db.Model):
    __tablename__ = 'parts_aplications'

    part_number = db.Column(db.String(100), db.ForeignKey(
        'part_numbers.part_number'), primary_key=True)

    aplication = db.Column(db.String(100), db.ForeignKey(
        'aplications.aplication'), primary_key=True)

    def __init__(self, part_number, aplication):
        self.part_number = part_number
        self.aplication = aplication

    def json(self):
        return {'part_number': self.part_number,
                'aplication': self.aplication}

    @classmethod
    def find_by_part_number(cls, part_number):
        return cls.query.filter_by(part_number=part_number).first()

    @classmethod
    def find_by_aplication(cls, aplication):
        return cls.query.filter_by(aplication=aplication).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
