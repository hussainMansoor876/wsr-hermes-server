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
import pandas as pd
import datetime

load_dotenv()

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


index_blueprint = Blueprint('admin', __name__)
mongo = PyMongo(app, retryWrites=False)

Cloud.config.update = ({
    'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET')
})


@index_blueprint.route("/getusers")
def getAllUsers():
    try:
        user = mongo.db.user
        result = user.find({'role': 'agent'}, {'password': 0}).sort("fname")
        data = []
        for x in result:
            x['_id'] = str(x['_id'])
            data.append(x)
        return jsonify({'data': data})
    except Exception as e:
        return jsonify({'data': str(e)})


@index_blueprint.route("/getAll", methods=["POST"])
def getAllData():
    subform = mongo.db.subform
    reqData = request.get_json(force=True)
    print(type(reqData['startDate']))
    sdate = reqData['startDate']
    edate = reqData['endDate']
    endDate = datetime.datetime(edate[0], edate[1] + 1, edate[2] + 1)
    startDate = datetime.datetime(sdate[0], sdate[1] + 1, sdate[2])
    result = subform.find({"timestamp": {'$lt': endDate, '$gte': startDate}})
    data = []
    for x in result:
        x['_id'] = str(x['_id'])
        data.append(x)
    print(data)
    return jsonify({'data': data})
