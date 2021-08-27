from db import db
from datetime import datetime

class NewModel(db.Model):
    __tablename__ = 'news'
    # -- Atributes --
    cod_new = db.Column(db.String(6), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    whom = db.Column(db.String(150))
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)

    # #Relation
    # tutoring_program = db.relationship('Tutoring_ProgramModel')
    #part_Teacher = db.relationship('PartBrandModel')

    def __init__(self, cod_new, title, description, whom, date_time,cod_tutoring_program):
        self.cod_new = cod_new
        self.title = title 
        self.description = description
        self.whom = whom
        self.date_time = date_time
        self.cod_tutoring_program = cod_tutoring_program

    def json(self):
        return {'cod_new': self.cod_new,
                'title': self.title,
                'description': self.description,
                'whom': self.whom,
                'date_time': self.date_time,
                'cod_tutoring_program': self.cod_tutoring_program
                }

    def update_data(self, cod_new, title, description, whom, date_time,cod_tutoring_program):
        self.cod_new = cod_new
        self.title = title 
        self.description = description
        self.whom = whom
        self.date_time = date_time
        self.cod_tutoring_program = cod_tutoring_program

    @classmethod
    def find_by_cod_new(cls, _cod_new):
        # -> SELECT * FROM items where cod_new=_cod_new LIMIT 1
        return cls.query.filter_by(cod_new=_cod_new).first()

    @classmethod
    def find_all(cls):
        # -> SELECT * FROM items
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()