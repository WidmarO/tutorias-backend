from db import db

class RoleModel(db.Model):
    __tablename__ = 'roles'
    
    # -- Attributes --
    # cod_role = db.Column(db.String(6), primary_key=True)
    role = db.Column(db.String(20), primary_key=True)

    # -- Relations --
    # user_role = db.relationship('UserRoleModel')
    
    user = db.relationship('UserModel') # test line

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
    def find_by_role(cls, _role):
        # -> SELECT * FROM items where cod_student=cod_student LIMIT 1
        return cls.query.filter_by(role=_role).first()

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
