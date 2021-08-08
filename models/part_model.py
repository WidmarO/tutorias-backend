from db import db


class PartModel_Model(db.Model):
    __tablename__ = 'parts_models'

    part_number = db.Column(db.String(100), db.ForeignKey(
        'part_numbers.part_number'), primary_key=True)

    model = db.Column(db.String(100), db.ForeignKey(
        'models.model'), primary_key=True)

    def __init__(self, part_number, model):
        self.part_number = part_number
        self.model = model

    def json(self):
        return {'part_number': self.part_number,
                'model': self.model}

    @classmethod
    def find_by_part_number(cls, part_number):
        # print(cls.query.filter_by(part_number=part_number))
        return cls.query.filter_by(part_number=part_number).first()

    @classmethod
    def find_by_model(cls, model):
        return cls.query.filter_by(model=model).first()

    @classmethod
    def find_equal_value(cls, part_number, model):
        return cls.query.filter_by(part_number=part_number).filter_by(model=model).first()

    @classmethod
    def get_list_part_number(cls, part_number):
        return cls.query.filter_by(part_number=part_number)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
