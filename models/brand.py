# from db import db


# class BrandModel(db.Model):
#     __tablename__ = 'brands'

#     brand = db.Column(db.String(100), primary_key=True)

#     part_brand = db.relationship('PartBrandModel')

#     def __init__(self, brand):
#         self.brand = brand

#     def json(self):
#         return {'brand': self.brand}

#     @classmethod
#     def find_by_brand(cls, brand):
#         return cls.query.filter_by(brand=brand).first()

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
