from flask import Blueprint, Flask, jsonify, request, Response
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import json
import bcrypt
import jwt
from flask_cors import CORS, cross_origin
import cloudinary as Cloud
from cloudinary import uploader

load_dotenv()

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


index_blueprint = Blueprint('subform', __name__)
mongo = PyMongo(app, retryWrites=False)

Cloud.config.update = ({
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET')
})


@index_blueprint.route("/signup", methods=["POST"])
def registerUser():
    add = mongo.db.user
    data = request.get_json(force=True)
    existUser = add.find_one({'email': data['email']})
    print(data)
    if(existUser):
        return jsonify({'success': False, 'message': 'User Already Exist!!!'})
    else:
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf8'), bcrypt.gensalt(12))
        encoded = jwt.encode(data, 'secretToken', algorithm='HS256')
        encoded = str(encoded).split("'")
        user = {
            'fname': data['fname'],
            'lname': data['lname'],
            'name': data['fname'] + data['lname'],
            'phone': data['phone'],
            'email': data['email'],
            'address': data['address'],
            'country': data['country'],
            'city': data['city'],
            'zip': data['zip'],
            'board': data['board'],
            'license': data['license'],
            'recruited': data['recruited'],
            'password': hashed_password,
            'secretToken': encoded[1],
            'role': 'agent'
        }
        add_data = add.insert_one(user)
        user['_id'] = str(add_data.inserted_id)
        del user['password']
        del user['secretToken']
        return jsonify({'success': True, 'message': 'Successfully Registered', "secretToken": 'encoded', 'email': data['email'], 'user': user})


