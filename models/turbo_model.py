from db import db


class TurboModel_Model(db.Model):
    __tablename__ = 'models'

    model = db.Column(db.String(100), primary_key=True)

    catalogue = db.relationship('CatalogueModel')

    def __init__(self, model):
        self.model = model

    def json(self):
        return {'model': self.model}

    @classmethod
    def find_by_model(cls, model):
        return cls.query.filter_by(model=model).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
