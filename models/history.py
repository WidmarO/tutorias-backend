from db import db


class HistoryModel(db.Model):
    __tablename__ = 'history'
    
    # -- Attributes --
    author = db.Column(db.String(100), nullable=False, unique=True, primary_key = True)
    action = db.Column(db.String(1000))
    role = db.Column(db.String(20), primary_key=True)

    # -- Relations --

    def __init__(self, author, role, action):
        self.author = author
        self.role= role
        self.action= action



    def json(self):
        return {'author': self.author,
                'role': self.role,
                'action': self.action
                }

    def update_data(self,author, role,action):
        self.author = author
        self.role= role
        self.action= action


    @classmethod
    def find_by_author(cls, _author):
        # -> SELECT * FROM items where author = _author LIMIT 1
        return cls.query.filter_by(author=_author)
    
    @classmethod
    def find_by_role(cls, _role):
        # -> SELECT * FROM items where role = _role LIMIT 1
        return cls.query.filter_by(role=_role)
            
    @classmethod
    def find_by_action(cls, _action):
        # -> SELECT * FROM items where action = _action LIMIT 1
        return cls.query.filter_by(action=_action)

    @classmethod
    def find_by_author_and_action(cls, _author, _action):
        return cls.query.filter_by(author=_author).filter_by(action=_action).first()

    @classmethod
    def find_by_author_and_role(cls, _author, _role):
        return cls.query.filter_by(author=_author).filter_by(role=_role).first()

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