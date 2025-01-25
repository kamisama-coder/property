from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from geopy.distance import geodesic
import requests
import base64
from math import radians, sin, cos, sqrt, atan2
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] =  os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy()
db.init_app(app)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String(250),nullable=False)
    address = db.Column(db.String(250),nullable=False)
    size = db.Column(db.String(250),nullable=False)
    price = db.Column(db.Integer,nullable=False)
    long = db.Column(db.Integer,nullable=False)
    latt = db.Column(db.Integer,nullable=False)
    price_suffix = db.Column(db.String(250),nullable=False) 
    cover = db.Column(db.LargeBinary,nullable=False)
    phone = db.Column(db.String(250),nullable=False)
    images = relationship('Picture', back_populates='property_relation')
    user_id = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(250),nullable=False)
    
class Picture(db.Model):
    __tablename__ = "pic"
    id = db.Column(db.Integer, primary_key=True)  
    property_relation = relationship('Post', back_populates='images')
    property_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    image = db.Column(db.LargeBinary,nullable=False)

with app.app_context():
    db.create_all()

def is_within_radius(center_lat, center_lon, point_lat, point_lon, radius_km):
    center_point = (center_lat, center_lon)
    point = (point_lat, point_lon)
    distance_km = geodesic(center_point, point).kilometers
    return distance_km <= radius_km

@app.route('/',  methods =["GET", "POST"])
def hello_world():
    if request.method == "POST":
       
       address = request.form.get("proxy_address")
       location = request.form.get("location")
       size = request.form.get("size")
       price = request.form.get("price")
       price_suffix = request.form.get("price_suffix")
       long =  request.form.get("long")
       latt =  request.form.get("latt")
       file = request.files.getlist('file')
       file2 = request.files['file2']
       phone =  request.form.get("number")
       user_id = request.form.get("id")
       status = request.form.get("status")
       new_user = Post(
            address=address,
            size=size,
            location=location,
            price=price,
            price_suffix=price_suffix,
            long = long,
            cover = file2.read(),
            latt = latt,
            phone = phone,
            user_id =  user_id,
            status = status
        )
       db.session.add(new_user)
       db.session.commit()
       for i in file:
        new_pic = Picture(
             image = i.read(),
             property_id = new_user.id,
         )    
        db.session.add(new_pic)
        db.session.commit()
       return render_template("index.html")
    return render_template("index.html")

@app.route('/search',  methods =["GET", "POST"])
def search():
    params = {
        "q": "new+york",
        "format":"json",
        "addressdetails":1,
        "polygon_geojson":0
    }    
    api =  "https://nominatim.openstreetmap.org/search?" 
    data = requests.get(api,params=params)
    response = data.json()
    return response

@app.route('/proficency',  methods =["GET", "POST"])
def prof():
     if request.method == "POST":
         property_dict = {}
         property_list = []
         size = request.form.get("size")
         price = request.form.get("price")
         long =  request.form.get("long")
         latt =  request.form.get("latt")
         status = request.form.get("status")
         price_suffix = request.form.get("price_suffix")
         results = db.session.query(Post).filter(Post.size == size, Post.price == price, Post.price_suffix == price_suffix, Post.status == status ).all()
         for i in results:
             judge = is_within_radius(latt, long, i.latt, i.long, 20)
             if judge == True:
                 base64_image = base64.b64encode(i.cover).decode('utf-8')
                 data_url = f"data:jpeg;base64,{base64_image}"
                 property_dict["cover"] = data_url
                 property_dict["data"] = i
                 property_list.append(property_dict)
         return render_template("fox.html", property_list=property_list)
        
     return render_template('finish.html')   

@app.route('/pic/<int:index>',  methods =["GET", "POST"])
def pic(index):
     results = db.session.query(Picture).all()
     pic_list = []
     for i in results:
         if i.property_relation.id == index:
           base64_image = base64.b64encode(i.image).decode('utf-8')
           data_url = f"data:jpeg;base64,{base64_image}"
           pic_list.append(data_url)
     return render_template("pic.html", pic_list = pic_list)

@app.route('/admin/<int:index>',  methods =["GET", "POST"])
def admin(index):
    admin = db.session.query(Post).filter(Post.user_id == index).all()
    return render_template("admin.html", admin = admin)

@app.route('/delete/<int:index>',  methods =["GET", "POST"])
def nope(index):
    works = db.session.query(Picture).filter(Picture.property_id == index).all()
    for work in works:
      db.session.delete(work)
      db.session.commit() 
    message = db.session.query(Post).filter(Post.id == index).first()
    importance = message.user_id
    db.session.delete(message)
    db.session.commit()    
    return redirect(url_for('admin', index=importance))
      

if __name__ == '__main__':
    app.run(debug=True)

