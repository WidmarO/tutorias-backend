from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
from models.brand import BrandModel
from Req_Parser import Req_Parser


# class Brand(Resource):
#   parser = Req_Parser()
#   parser.add_argument('id',esp_attr=True)  
#   parser.add_argument('brand',str, True)  

#   # @jwt_required()
#   def get(self, brand):
#     '''Search brand in the database and return it if is founded'''
#     brand = BrandModel.find_by_brand(brand)
#     if brand:
#       return brand.json()
#     return {'message': 'brand not found'},404
  
#   def post(self, brand):
#     print(request.json)
#     '''Add or created a new brand in database if already them not exist'''
#     if BrandModel.find_by_brand(brand):
#       return {'message': "A brand: '{}' already exist in data base".format(brand)}

#     ans,data = Brand.parser.parse_args(dict(request.json))
#     if not ans:
#       return data

#     brand = BrandModel(**data)

#     try:
#       brand.save_to_db()
#     except:
#       return {'message': "An error ocurred adding the brand"}, 500

#     return brand.json(),201

  # def delete(self, brand):
  #   '''Delete a brand from database if exist in it'''
  #   brand = BrandModel.find_by_brand(brand)
  #   if brand:
  #     brand.delete_from_db()      
  #     return brand.json(),200

  #   return {'message': 'Brand not found.'}
 
  # def put(self, dni):    

  #   ans, data = Client.parser.parse_args(dict(request.json))  
  #   if not ans:
  #     return data

  #   client = ClientModel.find_by_dni(dni)

  #   if client:
  #     client.update_data(**data)
      
  #   else:
  #     return {'message':"client not found."}

  #   client.save_to_db()
  #   client_list = ClientList()
  #   return client_list.get()


class BrandList(Resource):
  parser = Req_Parser()
  parser.add_argument('id',esp_attr=True)  
  parser.add_argument('brand',str, True)  
  # @jwt_required()  
  def get(self):    
    return list(map(lambda x: x.json(), BrandModel.query.all()))
  
  def post(self):

    print(request.json)
    brand = request.json['brand']
    '''Add or created a new brand in database if already them not exist'''
    if BrandModel.find_by_brand(brand):
      return {'message': "A brand: '{}' already exist in data base".format(brand)}

    ans,data = BrandList.parser.parse_args(dict(request.json))
    if not ans:
      return data

    brand = BrandModel(**data)

    try:
      brand.save_to_db()
    except:
      return {'message': "An error ocurred adding the brand"}, 500

    return brand.json(),201

  def delete(self):
    
    brand = request.json['brand']
    '''Delete a brand from database if exist in it'''
    brand = BrandModel.find_by_brand(brand)
    if brand:
      brand.delete_from_db()      
      return brand.json(),200

    return {'message': 'Brand not found.'}
  