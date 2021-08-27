from db import db


class UserModel(db.Model):
  __tablename__ = 'users'

  # -- Atributes --
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), nullable=False)
  password = db.Column(db.String(20), nullable=False)

  # -- Relations --   
  user_role = db.relationship('UserRoleModel')

  def __init__(self, id, username, password):
    self.id = id
    self.username = username
    self.password = password

  def json(self):
    return {'id': self.id,
            'username': self.username,   
            'password': self.password
            }

  def update_data(self, username, password):
    self.username = username
    self.password = password

  
  @classmethod
  def find_by_id(cls, _id):
    '''Devuelve desde la bd el usuario con el id recibido como parametro'''
    return cls.query.filter_by(id=_id).first()

  @classmethod
  def find_by_username(cls, _username):
    '''Devuelve desde la bd el usuario con el username recibido como parametro'''
    return cls.query.filter_by(username=_username).first()

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