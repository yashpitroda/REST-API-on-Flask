from distutils.log import debug
from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId #_id value is genrate
from werkzeug.security import generate_password_hash, check_password_hash
# import pymongo

app=Flask(__name__)
app.secret_key='secretkey'
app.config['MONGO_URI']='mongodb://localhost:27017/flaskcrudmongo' #give database here

mongo=PyMongo(app)
print(mongo)

#------------------------
@app.route('/add',methods=['POST'])
def add_user():
    try:
        id=mongo.db.users.insert_one({'name':'yash'})
        # id=mongo.db.Flask_mongo.insert_one({'name':'shivu'})
        return {'status':'sucess'}, 200
    except Exception as e:
        print(e)
        return {'status':'fail'},400
    

if __name__ == "__main__":
    app.run(debug=True)
    

     