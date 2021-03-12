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

from models.part_number import PartNumberModel
from models.turbo_model import TurboModel_Model
from models.brand import BrandModel
from models.motor import MotorModel
from models.aplication import AplicationModel
from models.catalogue import CatalogueModel
from models.category import CategoryModel
from models.product import ProductModel
from models.provider import ProviderModel
from models.purchase import PurchaseModel
from models.purchase_detail import PurchaseDetailModel

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
api.add_resource(BrandList, '/brands')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
