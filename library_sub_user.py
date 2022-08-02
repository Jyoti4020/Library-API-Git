

import json
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, true,func
from dataclasses import dataclass


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Myroot.20@localhost:3306/python_test'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@dataclass
class Library(db.Model):
    
    __tablename__='Library'
    id : int
    name : str
    address : str
    phone : str
          
    id = db.Column(db.Integer, primary_key=true)
    name = db.Column(db.String(50))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(15))
    user = db.relationship('Subscription_users')
    
    def __init__(self,id,name,address,phone): 
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        
@dataclass        
class User(db.Model):
    __tablename__='User'
    id : int
    name : str
    city : str
     
    id = db.Column(db.Integer, primary_key =true)
    name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    user = db.relationship('Subscription_users')
    
    def __init__(self,id,name,city):
        self.id = id
        self.name = name
        self.city = city
        
@dataclass        
class Subscription_users(db.Model):
    __tablename__='Subscription_users'
    
    id = int
    library_id : int
    user_id : int
    
    id = db.Column(db.Integer, primary_key =true)
    library_id = db.Column(db.Integer, db.ForeignKey('Library.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
   
    def __init__(self,id,library_id,user_id):
        self.id = id
        self.library_id = library_id
        self.user_id = user_id
        
## insert data in sub_user
@app.route('/library/<int:lib_id>/<int:user_id>/subuser',methods = ["POST"])
def insert_sub_user(lib_id,user_id):    
    sub = request.get_json()
    new_sub = Subscription_users(sub["id"],lib_id,user_id) 
    db.session.add(new_sub)
    db.session.commit()
    return(" sub_user added ")

# 1. get users in one library data 
# @app.route('/library/<int:lib_id>/user')
# def get_lib_user(lib_id):   
#     user_data = Subscription_users.query.filter_by(library_id = lib_id).all() 
#     return jsonify(user_data) 
   
# 2.get list of user_id in particular library 
# @app.route('/library/<int:lib_id>/user')
# def get_users(lib_id): 
#     user = {}
#     user_list = []
#     user_data = Subscription_users.query.filter_by(library_id = lib_id).with_entities(Subscription_users.user_id).all() 
#     for users in user_data :
#         user_list.append(users.user_id)           
#     user.update({"user_id " :user_list})
#     return jsonify(user)   

## get list of user details in particular Library
@app.route('/library/<int:lib_id>/user')
def get_users(lib_id): 
    user_dict = {}    
    user_list = []
    user_data = Subscription_users.query.filter_by(library_id = lib_id).with_entities(Subscription_users.user_id,User.id,User.name,User.city).all() 

    for users in user_data :
        user = {}
        if users.user_id == users.id :            
            user.update({"Id" : users.user_id})    
            user.update({"name" : users.name})     
            user.update({"city" : users.city}) 
            user_list.append(user)       
              
    user_dict.update({"Number of users in Details: " : user_list})
    return jsonify(user_dict)   

 
## get all library by one users
# 1.
# @app.route('/user/<int:u_id>/library')
# def get_user_wise_lib(u_id):    
#     lib_user_data = Subscription_users.query.filter_by(user_id = u_id).all()
#     return jsonify(lib_user_data)  
# 2. 
@app.route('/user/<int:u_id>/library')
def get_user_wise_lib(u_id): 
    library = {}
    lib_list = []
    lib_user_data = Subscription_users.query.filter_by(user_id = u_id).with_entities(Subscription_users.library_id).all()
    for lib in lib_user_data:
        lib_list.append(lib.library_id)           
    library.update({"library_id " : lib_list})
    return jsonify(library)   
  

if __name__ == '__main__':
    
    db.create_all()
    db.session.commit()
    app.run()
    
    
