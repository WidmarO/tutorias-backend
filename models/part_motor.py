from db import db


class PartMotorModel(db.Model):
    __tablename__ = 'parts_motors'

    part_number = db.Column(db.String(100), db.ForeignKey(
        'part_numbers.part_number'), primary_key=True)

    motor = db.Column(db.String(100), db.ForeignKey(
        'motors.motor'), primary_key=True)

    def __init__(self, part_number, motor):
        self.part_number = part_number
        self.motor = motor

    def json(self):
        return {'part_number': self.part_number,
                'motor': self.motor}

    @classmethod
    def find_by_part_number(cls, part_number):
        return cls.query.filter_by(part_number=part_number).first()

    @classmethod
    def find_by_motor(cls, motor):
        return cls.query.filter_by(motor=motor).first()

    @classmethod
    def find_equal_value(cls, part_number, motor):
        return cls.query.filter_by(part_number=part_number).filter_by(motor=motor).first()

    @classmethod
    def get_list_part_number(cls, part_number):
        return cls.query.filter_by(part_number=part_number)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
