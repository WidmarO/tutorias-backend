from db import db
import datetime


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    part_number = db.Column(db.String(100), db.ForeignKey(
        'part_numbers.part_number'), nullable=False)
    category = db.Column(db.String(100), db.ForeignKey(
        'categories.category'),  nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float(precision=2))
    sale_price = db.Column(db.Float(precision=2))

    purchase_detail = db.relationship('PurchaseDetailModel')

    def __init__(self, part_number, category, stock, purchase_price, sale_price):
        aux = ProductModel.query.all()

        self.part_number = part_number
        self.category = category
        self.stock = stock
        self.purchase_price = purchase_price
        self.sale_price = sale_price

    def json(self):
        return {'id': self.id,
                'part_number': self.part_number,
                'category': self.category,
                'stock': self.stock,
                'purchase_price': self.purchase_price,
                'sale_price': self.sale_price
                }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
