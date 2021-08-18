# from db import db


# class PartNumberModel(db.Model):
#     __tablename__ = 'part_numbers'

#     id = db.Column(db.Integer, unique=True, nullable=False)
#     part_number = db.Column(db.String(100), primary_key=True)

#     # relations
#     part_aplication = db.relationship('PartAplicationModel')
#     part_model = db.relationship('PartModel_Model')
#     part_brand = db.relationship('PartBrandModel')
#     part_motor = db.relationship('PartMotorModel')

#     product = db.relationship('ProductModel')

#     def __init__(self, id, part_number):
#         self.id = id
#         self.part_number = part_number

#     def json(self):
#         return {'id': self.id,
#                 'part_number': self.part_number}

#     @classmethod
#     def find_by_part_number(cls, part_number):
#         return cls.query.filter_by(part_number=part_number).first()

#     @classmethod
#     def find_by_id(cls, id):
#         return cls.query.filter_by(id=id).first()

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
