from db import db


class UserModel(db.Model):
  __tablename__ = 'users'

  # -- Atributes --
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(200), nullable=False)
  password = db.Column(db.String(256), nullable=False)
  role = db.Column(db.String(20), db.ForeignKey('roles.role'))


  # -- Relations --   
  # user_role = db.relationship('UserRoleModel') # test line

  def __init__(self, username, password, role):   
    self.username = username
    self.password = password
    self.role = role

  def json(self):
    return {'id': self.id,
            'username': self.username,   
            # 'password': self.password
            'role': self.role
            }

  def update_data(self, username, password, role):
    self.username = username
    self.password = password
    self.role = role

  @classmethod
  def find_by_id(cls, _id):
    '''Devuelve desde la bd el usuario con el id recibido como parametro'''
    return cls.query.filter_by(id=_id).first()

  @classmethod
  def find_by_username(cls, _username):
    '''Devuelve desde la bd el usuario con el username recibido como parametro'''
    return cls.query.filter_by(username=_username).first()

  @classmethod
  def find_by_role(cls, _role):
    '''Devuelve desde la bd el usuario con el rol recibido como parametro'''
    return cls.query.filter_by(role=_role)

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