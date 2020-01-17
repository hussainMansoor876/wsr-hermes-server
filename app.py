from flask import Flask,\
render_template, url_for, \
redirect, request, session, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import bcrypt
import os


load_dotenv()

from flask_cors import CORS, cross_origin
from routes import login, article, get, update

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app, retryWrites=False)

CORS(app, allow_headers = ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)

app.register_blueprint(login.index_blueprint, url_prefix='/login')
app.register_blueprint(article.article_blueprint, url_prefix='/article')
app.register_blueprint(get.get_blueprint, url_prefix='/get')
app.register_blueprint(update.update_blueprint, url_prefix='/update')

@app.route('/')
def index():
    return jsonify({ "message" : "Wellcome To RESTFUL APIs"})





if __name__=="__main__":
    app.run(debug=True)