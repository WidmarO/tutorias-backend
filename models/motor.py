from db import db


class MotorModel(db.Model):
    __tablename__ = 'motors'

    motor = db.Column(db.String(100), primary_key=True)

    catalogue = db.relationship('CatalogueModel')

    def __init__(self, motor):
        self.motor = motor

    def json(self):
        return {'motor': self.motor}

    @classmethod
    def find_by_motor(cls, motor):
        return cls.query.filter_by(motor=motor).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
