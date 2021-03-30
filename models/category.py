from db import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    category = db.Column(db.String(100), primary_key=True)

    product = db.relationship('ProductModel')

    def __init__(self, category):
        self.category = category

    def json(self):
        return {'category': self.category}

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
