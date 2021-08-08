import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity
from resources.user import UserRegister
from resources.client import Client, ClientList
from resources.brands import BrandList
from resources.aplications import AplicationList
from resources.motors import MotorList
from resources.part_numbers import PartNumberList
from resources.turbo_models import ModelList
# from resources.catalogue import CatalogueList, Catalogue
from resources.employees import Employee, EmployeeList
from resources.categories import CategoryList
from resources.products import ProductList, Product
from resources.dnis import DNI
from resources.turbos import Turbos
from resources.parts_models import Parts_Models

from models.part_number import PartNumberModel
from models.turbo_model import TurboModel_Model
from models.brand import BrandModel
from models.motor import MotorModel
from models.part_number import PartNumberModel
from models.aplication import AplicationModel
from models.part_model import PartModel_Model
from models.part_brand import PartBrandModel
from models.part_motor import PartMotorModel
from models.part_aplication import PartAplicationModel
# from models.catalogue import CatalogueModel
from models.aplication import AplicationModel
from models.category import CategoryModel
from models.product import ProductModel
from models.provider import ProviderModel
from models.purchase import PurchaseModel
from models.purchase_detail import PurchaseDetailModel
from models.employee import EmployeeModel
from models.category import CategoryModel


app = Flask(__name__)
CORS(app)
# ----------------------------- LOCAL DATABASE
# type_database = 'mysql'
# user_database = 'debian-sys-maint'
# pass_database = 'GO8LL0RrW418O2aA'
# url_database = 'localhost'
# name_database = 'turbos-flask-db'
# ---------------------------- CLEVER CLOUD DATABASE
type_database = 'mysql'
user_database = 'ulhu5xo4wswpfeyf'
pass_database = '7tZdO2gAvsCnUT2x8vr9'
url_database = 'bxtmrf8q1ibe3wcmvyie-mysql.services.clever-cloud.com'
name_database = 'bxtmrf8q1ibe3wcmvyie'

sqlalchemy_database_uri = type_database + '://' + user_database + \
    ':' + pass_database + '@' + url_database + '/' + name_database

app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'widmar'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(ClientList, '/clients')
# http://127.0.0.1:5000/user/1
api.add_resource(Client, '/client/<string:dni>')
api.add_resource(UserRegister, '/register')
# turbos
api.add_resource(ModelList, '/models')
api.add_resource(BrandList, '/brands')
api.add_resource(PartNumberList, '/parts')
api.add_resource(MotorList, '/motors')
api.add_resource(AplicationList, '/aplications')
api.add_resource(Turbos, '/turbos')
api.add_resource(Parts_Models, '/parts_models')
# api.add_resource(Catalogue, '/turbos/<int:id>')
# api.add_resource(CatalogueList, '/turbos')
api.add_resource(Employee, '/employee/<string:dni>')
api.add_resource(EmployeeList, '/employees')
api.add_resource(CategoryList, '/categories')
api.add_resource(ProductList, '/products')
api.add_resource(Product, '/product/<int:id>')
api.add_resource(DNI, '/dni')


# @app.before_first_request
# def create_tables():
#     db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
