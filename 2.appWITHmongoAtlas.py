from collections import UserList
from crypt import methods
from distutils.log import debug
from email import message
from urllib import response
from wsgiref.util import request_uri
from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId #_id value is genrate
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo

app=Flask(__name__)
app.secret_key='secretkey'

#------------------------
CONNECTION_STRING='mongodb+srv://yash:1234@cluster1.qwbqfwl.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING) 
database = client.get_database('flaskCRUDmongoAtlasDB') #create or inislize database
# usercollection = pymongo.collection.Collection(database, 'usercollection') #usercollection -- both side name same

#------------TESTING---------
@app.route('/testadd',methods=['POST'])
def testadd():
    try:
        #perform any opration : databasename.collectionName : if both or any one name(db or collection name) are not exsit then it automatic add
        id=database.testusercollection.insert_one({'name':"lalu"}) #usercollection is name of collection
        print(database.testusercollection.count_documents({}))
        print(database.usercollection.count_documents({}))
        return {'status':'sucess'}, 200
    except Exception as e:
        print(e)
        return {'status':'fail'},400
    
#get all data in connetion
@app.route('/testfatchdatafromserver')
def test_fatch_data_from_server():
    try:
        #here we fach how many document are preant in perticuler colletion
        response=database.usercollection.find({})
        response2=database.testusercollection.find({})
        # print(response) -- not working
        for i in response:
            print(i)
        print("--------------response2---------------")
        for i in response2:
            print(i)
        # return response, 200
        return {'status':'sucess'}, 200
    except Exception as e:
        print(e)
        return {'status':'fail'},400

#take data from user or client
@app.route('/testfatchdatafromclient',methods=['POST'])
def test_fatch_data_from_client():
    try:
        #mean cliect pase json rady che so e json hal _json ma che and ene fachkarye chie
        #write in body(in thender client): {"name":"amhi"}
        _json=request.get_json()
        print(_json)
        return {'status':'sucess'}, 200
    except Exception as e:
        print(e)
        return {'status':'fail','error':e}, 400
    
    
#------------project---------
@app.route('/add',methods=['POST'])
def add_user():
        _json=request.get_json()
        print(_json)
        _uname=_json['name']
        _uemail=_json['email']
        _upassword=_json['password']
        if _uname and _uemail and _upassword and request.method=='POST':
            _hash_password=generate_password_hash(_upassword)
            id=database.usercollection.insert_one({'name':_uname,'email':_uemail,'password':_hash_password})
            
            resp=jsonify('user added successfully')
            resp.status_code=200
        # return {'status':'sucess'}, 200
            return resp
        else:
            return not_found()

@app.route('/usersdata')
def users_data():
    #show all users in these collection
       usersdata=database.usercollection.find()
       #jem mysql ma commit hatu em ama dump use karvanu che
       userslist=dumps(usersdata) #dumps : is used to convert all the collectiondata(usersdata) to list form:[] :[{user1},{user2}]
       print(userslist)
       resp = jsonify(userslist) #in client server we comunicate with json #list is wrap with {}
       return userslist #it return only list: [] :[{},{}]
    # or
    #    return resp #retrun a list in json form {[]} :{[{},{}]}

#show one user from that id  
@app.route('/userdata/<id>') # <> : mean we take id dynamicaly as a value
def user_data(id):
    #show  user in these collection which id is match
       findeduserdata=database.usercollection.find({'_id':ObjectId(id)})
       #dump is used to comvert findeduserdata to list format 
       findeduserlist=dumps(findeduserdata) #dumps : is used to convert all the userdata(finded) to list form:[] :[{user1},{user2}]
       print(findeduserlist)
       resp = jsonify(findeduserlist) #in client server we comunicate with json #list is wrap with {}
       return findeduserlist #it return only list: [] :[{},{}]
    # or
    #    return resp #retrun a list in json form {[]} :{[{},{}]}
    
@app.route('/deleteuser/<id>', methods=['DELETE']) # <> : mean we take id dynamicaly as a value
def delete_user(id):
       database.usercollection.delete_one({'_id':ObjectId(id)})
       resp=jsonify('user deleted successfully')
       resp.status_code=200
       return resp
   
@app.route('/updateuser/<id>', methods=['PUT']) # <> : mean we take id dynamicaly as a value
def update_user(id):
    #condition
    ConditionValue={'_id':ObjectId(id)}
    #request
    _json=request.get_json()
    print(_json)
    #note - reset all value again
    _upname=_json['name']
    _upemail=_json['email']
    _uppassword=_json['password']
    _up_hash_password=generate_password_hash(_uppassword)
    #setvalue
    setValue={'$set':{'name':_upname,'email':_upemail,'password':_up_hash_password}}
    if _upname and _upemail and _uppassword and request.method=='PUT':
        database.usercollection.update_one(ConditionValue,setValue)
        resp=jsonify('user update successfully')
        resp.status_code=200
        return resp
    else:
        return not_found()
           
       
@app.errorhandler(404)
def not_found(error=None):
    massage={
        'status':404,
        'message':'not found'+request.uri
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp
        
        
        
if __name__ == "__main__":
    app.run(debug=True)
    

     