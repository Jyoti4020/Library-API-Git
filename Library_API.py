

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
    dept = db.relationship('Department') 
   
    def __init__(self,id,name,address,phone): 
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        
@dataclass        
class Department(db.Model):   
     
    __tablename__='Department'
    id : int
    name : str
    library_id : int
    
    id = db.Column(db.Integer, primary_key =true)
    name = db.Column(db.String(50))
    library_id = db.Column(db.Integer, db.ForeignKey('Library.id'))      
    books = db.relationship('Book') 
    
    def __init__(self,id,name,library_id):
        self.id = id
        self.name = name
        self.library_id = library_id
        
@dataclass        
class Book(db.Model):
    __tablename__='Book'
    id : int
    name : str
    price : str
    publication : str
    dept_id : int
     
    id = db.Column(db.Integer, primary_key =true)
    name = db.Column(db.String(50))
    price = db.Column(db.String(50))
    publication = db.Column(db.String(50))
    dept_id = db.Column(db.Integer, db.ForeignKey('Department.id'))
    
    def __init__(self,id,name,price,publication,dept_id):
        self.id = id
        self.name = name
        self.price = price
        self.publication = publication
        self.dept_id = dept_id

@dataclass        
class User(db.Model):
    __tablename__='User'
    id : int
    name : str
    city : str
     
    id = db.Column(db.Integer, primary_key =true)
    name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    #user = db.relationship('Subscription_users')

    def __init__(self,id,name,city):
        self.id = id
        self.name = name
        self.city = city
        

@app.route('/library')
## get all library table data
def get_library():
    lib_data = Library.query.all()
    return jsonify(lib_data)

## group by libraryId in dept
# @app.route('/lib/dept/re')
# def group_lib():   
#     records = db.session.query(Department,func.count(Department.id)).group_by(Department.library_id).all()  
#     return json.dumps(records)

## insert data in library
@app.route('/library',methods = ["POST"])
def insert_lib():    
    lib = request.get_json()
    new_lib = Library(lib["id"],lib["name"],lib["address"],lib['phone']) #,lib['user_id'])
    db.session.add(new_lib)
    db.session.commit()
    return(" Library added ")

## update lib with id 
@app.route('/library/<int:id>', methods=["PUT"])
def update_lib(id):
    if Library.query.get(id) is not None:
        lib = Library.query.get(id)
        name = request.json['name']
        add = request.json['address']
        phone = request.json['phone']
        lib.name = name
        lib.address = add
        lib.phone = phone
        db.session.commit()
        return ("Library has been Updated")
    else:
        return("Library not available")
## 2.update
@app.route('/library/', methods=["PUT"])
def update2_lib():
    lib = Library.query.filter_by(name='M.J library').first()
    lib.phone = "7621458610"
    db.session.commit()
    return ("Library has been Updated")
   
# delete library   
@app.route('/library/<int:id>', methods=["DELETE"])
def del_lib(id):
    if Library.query.get(id) is not None:
        lib = Library.query.get(id)
        db.session.delete(lib)
        db.session.commit()
        return("Library Deleted")
    else:
        return("Library not available")

## get all department in particular library
@app.route('/library/<int:lib_id>/dept')
def get_dept(lib_id):    
    dept_data = Department.query.filter_by(library_id = lib_id).all()
    return jsonify(dept_data)    
    
## insert dept in particular Library_id
@app.route('/library/<int:lib_id>/dept',methods = ["POST"])
def insert_dept(lib_id):    
    dept = request.get_json()
    new_dept = Department(dept["id"],dept["name"],lib_id)
    db.session.add(new_dept)
    db.session.commit()
    return(" Department added ")


## get all book in particular Dept_id
@app.route('/library/<int:dep_id>/book')
def get_book(dep_id):
    bookdata = Book.query.filter_by(dept_id = dep_id).all()
    return jsonify(bookdata)

## insert book in particular department
@app.route('/library/<int:dep_id>/book',methods = ["POST"])
def insert_book(dep_id):    
    book = request.get_json()
    new_book = Book(book["id"],book["name"],book["price"],book['publication'],dep_id)
    db.session.add(new_book)
    db.session.commit()
    return(" Book added ")


## get all user data
@app.route('/library/user')
def get_user():
    data = User.query.all()
    return jsonify(data)
 
## insert data in user table
@app.route('/library/user',methods = ["POST"])
def insert_user():    
    user = request.get_json()
    new_user = User(user["id"],user["name"],user["city"])
    db.session.add(new_user)
    db.session.commit()
    return("User has been inserted")


if __name__ == '__main__':
    
    db.create_all()
    db.session.commit()
    app.run()
    
    
 
