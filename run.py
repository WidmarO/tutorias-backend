from app import app
from db import db
from models.user import UserModel
from models.role import RoleModel
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
    roles = ['coordinator', 'tutor', 'principal', 'student', 'student_helper']
    for role in roles:
        try: 
            _role = RoleModel(role)
            _role.save_to_db()
        except:
            print('One error ocurred when create the roles')
    try:
        user = UserModel('admin','admin','coordinator')
        user.save_to_db()
    except:
        print('One error ocurred when create the admin user')


