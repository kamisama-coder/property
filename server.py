from flask import Flask,request,render_template,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from geopy.distance import geodesic
import requests
import base64
from math import radians, sin, cos, sqrt, atan2
from sqlalchemy.orm import relationship
from google import genai
from dotenv import load_dotenv
import torch
import overpy
import simplejson as json1
from flask_cors import CORS
import json
from io import BytesIO
from PIL import Image
import clip
import os

load_dotenv()

reform = []

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] =  os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy()
db.init_app(app)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer,primary_key=True)
    address = db.Column(db.String(250),nullable=False)
    size = db.Column(db.Integer,nullable=False)
    bhk = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer,nullable=False)
    long = db.Column(db.Integer,nullable=False)
    latt = db.Column(db.Integer,nullable=False)
    price_suffix = db.Column(db.String(250),nullable=False) 
    cover = db.Column(db.LargeBinary,nullable=False)
    phone = db.Column(db.String(250),nullable=False)
    images = relationship('Picture', back_populates='property_relation')
    user_id = db.Column(db.String(250),nullable=False)
    status = db.Column(db.String(250),nullable=False)
    proxy_address = db.Column(db.String(250),nullable=False)

class Picture(db.Model):
    __tablename__ = "pic"
    id = db.Column(db.Integer, primary_key=True)  
    property_relation = relationship('Post', back_populates='images')
    property_string = db.Column(db.String(250), nullable=False)
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
            json_data = request.form.get("form")
            data = json.loads(json_data)

            index = data.get("id")
            address = data.get("address")  # fixed
            size = data.get("area_sqft")
            price = data.get("price")
            bhk = data.get("size")  # if you add this field in the form
            price_suffix = data.get("price_suffix")
            long = data.get("long")
            latt = data.get("latt")
            phone = data.get("phone")  # fixed
            status = data.get("status")
            proxy_address = data.get("proxy_address")
   
            cover_file = request.files.getlist('cover[]')
            if not cover_file:
                return jsonify({"error": "Missing cover image"}), 400

            new_user = Post(
                address=address,
                size=size,
                price=price,
                price_suffix=price_suffix,
                long=long,
                latt=latt,
                phone=phone,
                user_id=index,
                status=status,
                bhk=bhk,
                cover=cover_file[0].read(),
                proxy_address=proxy_address
            )

            db.session.add(new_user)
            db.session.commit()
            
            for key in request.files:
                files = request.files.getlist(key)
                if(key == "cover[]"):
                    continue
                for image in files:

                    if image: 
                        new_pic = Picture(
                            image=image.read(),
                            property_id=new_user.id,
                            property_string=key.replace("[]", "")
                        )
                        db.session.add(new_pic)

            db.session.commit()


            return jsonify({"message": "Upload successful"}), 200

   
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
        property_list = []

        size = request.form.get("size")
        price = request.form.get("price")
        long = request.form.get("long")
        latt = request.form.get("latt")
        status = request.form.get("status")
        price_suffix = request.form.get("price_suffix")

        results = db.session.query(Post).filter(
            Post.size == size,
            Post.price == price,
            Post.price_suffix == price_suffix,
            Post.status == status
        ).all()

        for i in results:
            if is_within_radius(latt, long, i.latt, i.long, 20):
                base64_image = base64.b64encode(i.cover).decode('utf-8')
                data_url = f"data:image/jpeg;base64,{base64_image}"
                property_list.append({
                    "cover": data_url,
                    "data": {
                        "id": i.user_id,
                        "address": i.address,
                        "price": i.price,
                        "price_suffix": i.price_suffix,
                        "status": i.status,
                        "size": i.size,
                        "long": i.long,
                        "latt": i.latt
                    }
                })

        return jsonify(property_list)

    return jsonify({"message": "GET request received"})

@app.route('/pics', methods=["GET", "POST"])
def pic():
    index = int(request.args.get("index"))
    results = db.session.query(Picture).all()
    pic_list = []
    for i in results:
        print(i.property_relation.id)
        if i.property_relation.id == index:
            base64_image = base64.b64encode(i.image).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{base64_image}"
            pic_list.append(data_url)
    return jsonify(pic_list)

@app.route('/admin/<string:index>',  methods =["GET", "POST"])
def admin(index):
    admin = db.session.query(Post).filter(Post.user_id == index).all()
    return render_template("admin.html", admin = admin)


@app.route('/edit/<index>', methods=["GET", "POST"])
def nope(index):
    if request.method == "GET":
        posts = db.session.query(Post).filter(Post.id == index).all()

        store = []
        for post in posts:
            store.append({
                'id': post.user_id,
                'address': post.address,
                'size': post.size,
                'price': post.price,
                'price_suffix': post.price_suffix,
                'long': post.long,
                'latt': post.latt,
                'phone': post.phone,
                'status': post.status,
                'bhk': post.bhk,
                'proxy_address': post.proxy_address,
                'pics': []  # ✅ Initialize the 'pics' array
            })

        pics = db.session.query(Picture).filter(Picture.property_id == index).all()

        for it in pics:
            if it.property_string not in store[0]["pics"]:
                store[0]["pics"].append(it.property_string)

        return jsonify(store)
    if request.method == "POST":
        post = db.session.get(Post, index)
        json_data = request.form.get("form")
        data = json.loads(json_data)

        post.address = data.get("address", post.address)
        post.size = data.get("area_sqft", post.size)
        post.price = data.get("price", post.price)
        post.bhk = data.get("size", post.bhk)
        post.price_suffix = data.get("price_suffix", post.price_suffix)
        post.long = data.get("long", post.long)
        post.latt = data.get("latt", post.latt)
        post.phone = data.get("phone", post.phone)
        post.status = data.get("status", post.status)
        post.proxy_address = data.get("proxy_address", post.proxy_address)
        cover_files = request.files.getlist('cover[]')

        if cover_files:
            post.cover = cover_files[0].read()

        db.session.commit()  

        pics = db.session.query(Picture).filter(Picture.property_id == index).all()
        for key in request.files:
                files = request.files.getlist(key)
                if(files != []):
                    for image in files:
                            new_pic = Picture(
                                image=image.read(),
                                property_id=index,
                                property_string=key.replace("[]", "")
                            )
                            db.session.add(new_pic)

        db.session.commit()
           

   

    
@app.route('/system_design', methods=["GET", "POST"])
def query():
    if request.method == "POST":
        api = overpy.Overpass()
        data = request.get_json()
        latitude = data['lat']
        print(latitude)
        longitude = data['lon']
        print(longitude)
        place_type = data['value']
        

        query = f"""
        (
        node
            ["amenity"="{place_type}"]
            (around:{5000},{latitude},{longitude});
        );
        out body;
        """

        storage = {}
        result = api.query(query)
        transport = []

        for node in result.nodes:
            name = node.tags.get("name", "Unnamed Place")
            print(f"{name} — Latitude: {node.lat}, Longitude: {node.lon}")
            transport.append({
                "name":name,
                "latitude": node.lat,
                "longitude": node.lon
            })    
        return jsonify(transport)
            
        
@app.route('/gemini',methods=["GET", "POST"])
def gemini():
    if request.method == "POST":
        global reform  # 👈 Reference it inside the function

        data = request.get_json()
        prompt = data["query"]
        client = genai.Client()

        raw_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
            You are an information extraction system. Given the prompt: "{prompt}", extract only the following keys if they are present:

            - size 
            - price   
            - location  
            - bhk  

            Rules:
            - Use "<" if the prompt says "less than", and ">" for "more than".
            - Use "-" if a range is mentioned (e.g., "1000-1500").
            - Given an input like "2 crore", "1.5 crore", or "50 lakh", return the corresponding integer value without commas or units.
            - Do not add any explanation or code.
            - Return only a Python dictionary (no comments or text).
            - Do NOT use markdown formatting like ```json.
            - Output must start directly with and be valid for json.loads()
            Output format:
            {{"key1": "value1", "key2": "value2", ...}}
            """
        )

        response = json.loads(raw_response.text)
        print(response)

        posts = db.session.query(Post)
        filters_applied = 0  

        if response.get('location'):
            keywords = response["location"].strip().lower().split()
            for index,word in enumerate(keywords):
                check = posts.filter(func.lower(Post.proxy_address).like(f"%{word}%"))
                if check.count() == 0 and index > 0:
                    continue
                posts = check
            filters_applied += 1

        if response.get('bhk'):
            size = str(response['bhk'])
            filters_applied += 1
            if size.startswith("<"):
                posts = posts.filter(Post.bhk < float(size[1:]))
            elif size.startswith(">"):
                posts = posts.filter(Post.bhk > float(size[1:]))
            elif "-" in size:
                low, high = map(float, size.split("-"))
                posts = posts.filter(Post.bhk.between(low, high))
            else:
                posts = posts.filter(Post.bhk == float(size))

        if response.get('price'):
            filters_applied += 1
            price = str(response['price'])
            if price.startswith("<"):
                posts = posts.filter(Post.price < float(price[1:]))
            elif price.startswith(">"):
                posts = posts.filter(Post.price > float(price[1:]))
            elif "-" in price:
                low, high = map(float, price.split("-"))
                posts = posts.filter(Post.price.between(low, high))
            else:
                posts = posts.filter(Post.price == float(price))

        if response.get('size'):
            filters_applied += 1
            size = str(response['size'])
            if size.startswith("<"):
                posts = posts.filter(Post.size < float(size[1:]))
            elif size.startswith(">"):
                posts = posts.filter(Post.size > float(size[1:]))
            elif "-" in size:
                low, high = map(float, size.split("-"))
                posts = posts.filter(Post.size.between(low, high))
            else:
                posts = posts.filter(Post.size == float(size))

        if filters_applied == 0:
            return jsonify({"error": "Please specify at least one filter (e.g., price, size, location, etc.)"})

        results = posts.all()
        if not results:
            return jsonify({"error": "No properties found matching the criteria."})

        property_list = []
        for i in results:
            data_url = f"data:image/jpeg;base64,{base64.b64encode(i.cover).decode('utf-8')}"
            property_list.append({
                "cover": data_url,
                "id": i.id,
                "address": i.address,
                "price": i.price,
                "price_suffix": i.price_suffix,
                "phone": i.phone,
                "bhk": i.bhk,
                "size": i.size,
                "long": i.long,
                "latt": i.latt
            })

        reform = property_list  # ✅ Set the global variable

        return jsonify(property_list)



@app.route('/system-server',methods=["GET", "POST"])
def server():
    return jsonify(reform)
        
    
@app.route('/clipsort', methods=["GET", "POST"])
def clipsort():
    data = request.get_json()
    query = data['query']

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
    Your task is to extract each place (e.g., "kitchen", "bedroom") from the following text: ({query})

    Return a **Python dictionary** where:
    - Each **key** is the place name in lowercase (e.g., "kitchen", "bedroom")
    - Each **value** is the full descriptive phrase for that place from the text

    ⚠️ Output requirements:
    - Only return a valid Python dictionary
    - Do NOT include any extra text or explanation
    - Do NOT use markdown formatting like ```json
    - Output must start directly with and be valid for json.loads()

    """
    )

    print(response.text)
    response_dict = json.loads(response.text)  
  

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    store = []  
    for i in range(0,len(reform)):
        store.append(reform[i]['id'])

   

    score = []

    for file_id in store:
        posts_query = db.session.query(Picture).filter(Picture.property_id == file_id)
        count = 0
        current_score = 0
        for place, place_query in response_dict.items():
            max_similarity = 0
            matching_posts = posts_query.filter(Picture.property_string.ilike(f"%{place}%")).all()
            if not matching_posts:
                count += 1
                continue
            else:
                for picture in matching_posts:
                    image = Image.open(BytesIO(picture.image)).convert("RGB")
                    image_input = preprocess(image).unsqueeze(0).to(device)
                    text_input = clip.tokenize(place_query).to(device)

                    with torch.no_grad():
                        image_features = model.encode_image(image_input)
                        text_features = model.encode_text(text_input)
                    similarity = (image_features @ text_features.T).squeeze().cpu().item()

                    if similarity > max_similarity:
                        max_similarity = similarity

                current_score += max_similarity
                count += 1

        avg_score = current_score / count 

        post = db.session.query(Post).filter(Post.id == file_id).first()
        base64_image = base64.b64encode(post.cover).decode('utf-8')
        data_url = f"data:image/jpeg;base64,{base64_image}"
        print(avg_score)

        score.append({
            "id": post.id,
            "score": avg_score,
            "cover": data_url,
            "address": post.address,
            "price": post.price,
            "price_suffix": post.price_suffix,
            "long": post.long,
            "latt": post.latt,
            "score":avg_score
        })

    score.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(score)

if __name__ == '__main__':
    app.run(debug=True)

