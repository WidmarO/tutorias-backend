from db import db

class User_RolesModel(db.Model):
    __tablename__ = 'user_roles'
    
    cod_user_role = db.Column(db.String(6), primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cod_role = db.Column(db.String(6), db.ForeignKey('roles.cod_role'))

    # #Relation
    # id = db.relationship('UsersModel')
    # roles=db.relationship('RolesModel')

    def __init__(self, cod_user_role, cod_role):
        self.cod_user_role = cod_user_role
        #self.id = id
        self.cod_role = cod_role

    def json(self):
        return {'cod_user_role': self.cod_user_role,
                #'id': self.id,
                'cod_role': self.cod_role
                }

    def update_data(self, cod_user_role, cod_role):
        self.cod_user_role = cod_user_role
        #self.id = id
        self.cod_role = cod_role

    @classmethod
    def find_by_cod_user_role(cls, _cod_user_role):
        # -> SELECT * FROM items where cod_student=cod_student LIMIT 1
        return cls.query.filter_by(cod_user_role=_cod_user_role).first()

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