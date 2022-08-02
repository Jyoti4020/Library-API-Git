
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
    # user_lib = db.relationship('Subscription_users')
    
    def __init__(self,id,name,address,phone): 
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone

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
    user_book = db.relationship("Book_wise_users")
    
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
    # user = db.relationship('Subscription_users')
    user_book = db.relationship("Book_wise_users")
    def __init__(self,id,name,city):
        self.id = id
        self.name = name
        self.city = city

@dataclass        
class Book_wise_users(db.Model):
    __tablename__='Book_wise_users'
    
    id = int
    book_id : int
    user_id : int
    
    id = db.Column(db.Integer, primary_key =true)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
   
    def __init__(self,id,book_id,user_id):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        
## insert data in book_wise_user
@app.route('/library/<int:book_id>/<int:user_id>/bookuser',methods = ["POST"])
def insert_book_wise_user(book_id,user_id):    
    book_user = request.get_json()
    new_book_user = Book_wise_users(book_user["id"],book_id,user_id) 
    db.session.add(new_book_user)
    db.session.commit()
    return("Book wise User added ")
 
# # 2.get list of books in particular User 
@app.route('/library/user/<int:user_id>/books')
def get_user_booklist(user_id): 
    book_dict = {}
    book_list = []
    book_data = Book_wise_users.query.filter_by(user_id = user_id).with_entities(Book_wise_users.book_id,Book.id,Book.name,Book.price,Book.publication).all() 
    for book in book_data :
        books = {}
        if book.book_id == book.id :
            books.update({"id" : book.book_id})    
            books.update({"name" : book.name})     
            books.update({"price" : book.price}) 
            books.update({"publication" : book.publication})
            
            book_list.append(books)   
                    
    book_dict.update({"Number of Books in Details " :book_list})
    return jsonify(book_dict) 


if __name__ == '__main__':
    
    db.create_all()
    db.session.commit()
    app.run()
    