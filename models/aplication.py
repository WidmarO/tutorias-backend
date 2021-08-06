from db import db


class AplicationModel(db.Model):
    __tablename__ = 'aplications'

    aplication = db.Column(db.String(100), primary_key=True)

    part_aplication = db.relationship('PartAplicationModel')

    def __init__(self, aplication):
        self.aplication = aplication

    def json(self):
        return {'aplication': self.aplication}

    @classmethod
    def find_by_aplication(cls, aplication):
        return cls.query.filter_by(aplication=aplication).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
