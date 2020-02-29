from flask import Flask,\
render_template, url_for, \
redirect, request, session, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import bcrypt
import os


# load_dotenv()

from flask_cors import CORS, cross_origin
# from routes import login, subform, admin
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://mansoor:mansoor11@wsr-hermes-shard-00-00-cxem6.mongodb.net:27017,wsr-hermes-shard-00-01-cxem6.mongodb.net:27017,wsr-hermes-shard-00-02-cxem6.mongodb.net:27017/test?ssl=true&replicaSet=WSR-Hermes-shard-0&authSource=admin&retryWrites=true&w=majority'


mongo = PyMongo(app)

CORS(app, allow_headers = ["Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Origin"], supports_credentials=True)


# app.register_blueprint(login.index_blueprint, url_prefix='/login')
# app.register_blueprint(subform.index_blueprint, url_prefix='/subform')
# app.register_blueprint(admin.index_blueprint, url_prefix='/admin')

@app.route('/')
def index():
    return jsonify({ "message" : "Wellcome To RESTFUL APIs"})





if __name__=="__main__":
    app.run(debug=True, port=3001)