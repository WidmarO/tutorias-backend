from db import db

class RoleModel(db.Model):
    __tablename__ = 'roles'
    
    cod_role = db.Column(db.String(6), primary_key=True)
    role = db.Column(db.String(20), nullable=False)

    #Relation
    user_role = db.relationship('UserRoleModel')

    def __init__(self, cod_role, role):
        self.cod_role = cod_role
        self.role = role

    def json(self):
        return {'cod_role': self.cod_role,
                'role': self.role
                }

    def update_data(self, cod_role, role):
        self.cod_role = cod_role
        self.role = role

    @classmethod
    def find_by_cod_role(cls, _cod_role):
        # -> SELECT * FROM items where cod_student=cod_student LIMIT 1
        return cls.query.filter_by(cod_role=_cod_role).first()

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
