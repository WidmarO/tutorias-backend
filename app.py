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
from resources.part_numbers import PartNumber, PartNumberList
from resources.turbo_models import ModelList
# from resources.catalogue import CatalogueList, Catalogue
from resources.turbos import Turbos
from resources.parts_models import Parts_Models
from resources.parts_brands import Parts_Brands


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
user_database = 'udwsw0hbqah0nikx'
pass_database = '6eaqlxBNvKWNGUuRR32M'
url_database = 'b0du4ayviyfhrlbnjckc-mysql.services.clever-cloud.com'
name_database = 'b0du4ayviyfhrlbnjckc'

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
api.add_resource(PartNumber, '/part/<int:id>')
api.add_resource(MotorList, '/motors')
api.add_resource(AplicationList, '/aplications')
api.add_resource(Turbos, '/turbos')
api.add_resource(Parts_Models, '/parts_models/<string:part_number>')
api.add_resource(Parts_Brands, '/parts_brands/<string:part_number>')
api.add_resource(Parts_Motors, '/parts_motors/<string:part_number>')
api.add_resource(Parts_Aplications, '/parts_aplications/<string:part_number>')
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
