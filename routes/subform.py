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
import datetime
import pandas as pd

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


@index_blueprint.route("/submission", methods=["POST"])
def registerUser():
    subform = mongo.db.subform
    data = request.form
    data = dict(data)
    del data['upload']
    fileData = request.files
    # existUser = add.find_one({'email': data['email']})
    data['files'] = []
    data['files'].append(uploader.upload(
            fileData['upload'],
            public_id = fileData["upload"].filename,
            resource_type="auto",
            use_filename=True,
            folder = f'Closings/{data["agentId"]}/{data["streetAddress"]}',
            chunk_size=1000000000))
    data['paidDate'] = pd.to_datetime(data['paidDate'])
    return jsonify({
        'success': True
    })
    #     add_data = add.insert_one(user)
    #     user['_id'] = str(add_data.inserted_id)
    #     del user['password']
    #     del user['secretToken']
    #     return jsonify({'success': True, 'message': 'Successfully Registered', "secretToken": 'encoded', 'email': data['email'], 'user': user})
