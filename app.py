from flask import Flask,\
render_template, url_for, \
redirect, request, session, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import bcrypt
import os


load_dotenv()

from flask_cors import CORS, cross_origin
from routes import login, subform, admin
app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')


mongo = PyMongo(app)

CORS(app, allow_headers = ["Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Origin"], supports_credentials=True)


app.register_blueprint(login.index_blueprint, url_prefix='/login')
app.register_blueprint(subform.index_blueprint, url_prefix='/subform')
app.register_blueprint(admin.index_blueprint, url_prefix='/admin')

@app.route('/')
def index():
    return jsonify({ "message" : "Wellcome To RESTFUL APIs"})





if __name__=="__main__":
    app.run(debug=True, port=3001)