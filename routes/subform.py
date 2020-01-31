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
    data['files'] = []
    data['files'].append(uploader.upload(
        fileData['upload'],
        public_id=fileData["upload"].filename,
        resource_type="auto",
        use_filename=True,
        folder=f'Closings/{data["agentId"]}/{data["streetAddress"]}',
        chunk_size=1000000000))
    data['paidDate'] = pd.to_datetime(data['paidDate'])
    data['review'] = False
    data['timestamp'] = datetime.datetime.now()
    try:
        add_data = subform.insert_one(data)
        return jsonify({
            'success': True
        })
    except Exception as e:
        print('e', e)
        return jsonify({
            'success': False,
            'message': str(e)
        })


@index_blueprint.route("/getAll")
def getAllData():
    subform = mongo.db.subform
    subform = subform.find({'review': False}).sort("timestamp", -1)
    data = []
    print(subform)
    for x in subform:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})
