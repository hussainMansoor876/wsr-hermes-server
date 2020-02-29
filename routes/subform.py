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
from bson.json_util import ObjectId
from pymongo import ReturnDocument

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
    data['soldPrice'] = json.loads(data['soldPrice'])
    data['transactionFee'] = json.loads(data['transactionFee'])
    data['paidAmount'] = json.loads(data['paidAmount'])
    data['zip'] = json.loads(data['zip'])
    fileData = request.files
    data['files'] = []
    if(fileData):
        print("Hello")
        for i in fileData.values():
            data['files'].append(uploader.upload(
                i,
                public_id=i.filename,
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
        return jsonify({
            'success': False,
            'message': str(e)
        })


@index_blueprint.route("/getAll")
def getAllData():
    subform = mongo.db.subform
    result = subform.find({'review': False}).sort("timestamp", -1)
    data = []
    for x in result:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})


@index_blueprint.route("/get-user/<id>")
def getUser(id):
    subform = mongo.db.subform
    print(id)
    result = subform.find({'agentId': id}).sort("timestamp", -1)
    data = []
    for x in result:
        x['_id'] = str(x['_id'])
        data.append(x)
    return jsonify({'data': data})


@index_blueprint.route("/del-file", methods=["POST"])
def delFile():
    data = request.get_json(force=True)
    subform = mongo.db.subform
    res = subform.update(
        {},
        {'$pull': {'files': data['file']}},
    )
    result = uploader.destroy(data['file']['public_id'])
    if(result['result'] == 'ok'):
        updateData = subform.find_one({"_id": ObjectId(data['_id'])})
        updateData['_id'] = str(updateData['_id'])
        return jsonify({'success': True, 'data': updateData})
    return jsonify({'success': False})


@index_blueprint.route("/approve", methods=["POST"])
def approve():
    subform = mongo.db.subform
    data = request.get_json(force=True)
    data['id'] = ObjectId(data['id'])
    result = subform.find_one_and_update(
        {'_id': data['id']}, {"$set": {"review": True}}, return_document=ReturnDocument.AFTER)
    if(result['review']):
        return jsonify({'success': True})


@index_blueprint.route("/update-form", methods=["POST"])
def updateForm():
    subform = mongo.db.subform
    data = request.form
    data = dict(data)
    data['soldPrice'] = json.loads(data['soldPrice'])
    data['transactionFee'] = json.loads(data['transactionFee'])
    data['paidAmount'] = json.loads(data['paidAmount'])
    data['zip'] = json.loads(data['zip'])
    fileData = request.files
    data['files'] = json.loads(data['files'])
    if(fileData):
        for i in fileData.values():
            data['files'].append(uploader.upload(
                i,
                public_id=i.filename,
                resource_type="auto",
                use_filename=True,
                folder=f'Closings/{data["agentId"]}/{data["streetAddress"]}',
                chunk_size=1000000000))
    data['paidDate'] = pd.to_datetime(data['paidDate'])
    data['review'] = True
    data['_id'] = ObjectId(data['_id'])
    try:
        subform.find_one_and_update({'_id': data['_id']}, {"$set": data})
        return jsonify({
            'success': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })


@index_blueprint.route("/update-agent-form", methods=["POST"])
def updateForm1():
    subform = mongo.db.subform
    data = request.form
    data = dict(data)
    data['soldPrice'] = json.loads(data['soldPrice'])
    data['transactionFee'] = json.loads(data['transactionFee'])
    data['paidAmount'] = json.loads(data['paidAmount'])
    fileData = request.files
    data['files'] = json.loads(data['files'])
    if(fileData):
        for i in fileData.values():
            data['files'].append(uploader.upload(
                i,
                public_id=i.filename,
                resource_type="auto",
                use_filename=True,
                folder=f'Closings/{data["agentId"]}/{data["streetAddress"]}',
                chunk_size=1000000000))
    data['paidDate'] = pd.to_datetime(data['paidDate'])
    data['_id'] = ObjectId(data['_id'])
    try:
        subform.find_one_and_update({'_id': data['_id']}, {"$set": data})
        return jsonify({
            'success': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })