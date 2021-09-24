from app import app
from db import db
from models.user import UserModel
from models.role import RoleModel
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()

