import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta


from models.role import RoleModel
from models.user import UserModel
from models.user_role import UserRoleModel

from models.coordinator import CoordinatorModel
from models.tutoring_program import TutoringProgramModel
from models.new import NewModel
from models.teacher import TeacherModel
from models.principal import PrincipalModel
from models.tutor import TutorModel
from models.student import StudentModel
from models.tutor_student import TutorStudentModel
from models.appointment import AppointmentModel
from models.student_helper import StudentHelperModel
from models.workshop import WorkshopModel
from models.workshop_student import WorkshopStudentModel
from models.student_helper_tutor import StudentHelperTutorModel
from models.workshop_attendance import WorkshopAttendanceModel
from models.curricular_advancement import CurricularAdvancementModel


from security import authenticate, identity
# from resources.user import UserRegister
# from resources.client import Client, ClientList
# from resources.brands import BrandList
# from resources.part_numbers import PartNumber, PartNumberList
# from resources.turbo_models import ModelList
# from resources.catalogue import CatalogueList, Catalogue
# from resources.parts_brands import Parts_Brands
from resources.documentation import Documentation
# from resources.student import StudentList, Student
# from resources.catalogue import CatalogueList, Catalogue
# from resources.parts_brands import Parts_Brands
# from resources.teacher import TeacherList,Teacher


app = Flask(__name__)
CORS(app)
# ----------------------------- LOCAL DATABASE
type_database = 'mysql'
user_database = 'root'
pass_database = 'root' # for wid is toor
url_database = 'localhost:3307' # for wid is 127.0.0.1
name_database = 'tutoring-system-bd'
# ---------------------------- CLEVER CLOUD DATABASE
# type_database = 'mysql'
# user_database = 'udwsw0hbqah0nikx'
# pass_database = '6eaqlxBNvKWNGUuRR32M'
# url_database = 'b0du4ayviyfhrlbnjckc-mysql.services.clever-cloud.com'
# name_database = 'b0du4ayviyfhrlbnjckc'

# -- Set de BD configurations for conection
sqlalchemy_database_uri = type_database + '://' + user_database + \
    ':' + pass_database + '@' + url_database + '/' + name_database
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -- Configurations for security
app.secret_key = 'widmar'
api = Api(app)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)  # /auth

# -- RESOURCES OF THE APPLICATION
api.add_resource(Documentation, '/')
# api.add_resource(ClientList, '/clients')
# api.add_resource(Client, '/client/<string:dni>')
# api.add_resource(UserRegister, '/register')
#api.add_resource(ModelList, '/models')
#api.add_resource(BrandList, '/brands')
# api.add_resource(TeacherList,'/teachers') #endpoint
# api.add_resource(Teacher,'/teacher/<string:cod_teach>')
#api.add_resource(PartNumberList, '/parts')
#api.add_resource(PartNumber, '/part/<int:id>')
#api.add_resource(Parts_Brands, '/parts_brands/<string:part_number>')

# -- Module that create the tables in the BD
#-- Module that create the tables in the BD.
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
