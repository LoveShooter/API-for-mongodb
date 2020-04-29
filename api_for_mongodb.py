#api_for_mongodb.py
#CRUD RESTApi with using Flask

import pymongo
import requests
import json, bson
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
#from pymongo import MongoClient


app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'to-do-lists' # name of database on mongo
app.config["MONGO_URI"] = "mongodb+srv://sysadm:Ff121314@cluster0-gpxwq.mongodb.net/to-do-lists"

mongo = PyMongo(app)



@app.route('/getdata', methods=['GET'])  # find all data in my collection
def get_all_data():
    todos = mongo.db.todos #connect to my collection

    output = []

    for q in todos.find():   # q - like query
        output.append({'userId': q['userId'], 'id': q['id'], 'title': q['title'], 'completed': q['completed']})

    return jsonify({'result': output})



@app.route('/getdata/<status>', methods=['GET'])
def get_one_data(status):
    todos = mongo.db.todos
    q = todos.find_one({'completed': status}) # find title
    if q:
        output = {'userId': q['userId'], 'id': q['id'], 'title': q['title'], 'completed': q['completed']}
    else:
        output = 'No results found!'

    return jsonify({'result': output})



@app.route('/adddata', methods=['POST']) # add data in db. Need input JSON-like data.
def add_data():
    todos = mongo.db.todos
    
    _userId = request.json['userId']
    _id = request.json['id']
    _title = request.json['title']
    _completed = request.json['completed']

    todos_id = todos.insert({'userId': _userId, 'id': _id, 'title': _title, 'completed': _completed})
    new_todos = todos.find_one({'_id': todos_id})

    output = {'userId': new_todos['userId'], 'id': new_todos['id'], 'title': new_todos['title'], 'completed': new_todos['completed']}

    return jsonify({'result': output})




@app.route('/deldata/<deltatus>', methods=['DELETE'])
def del_one_data(delstatus):
    todoscoll = mongo.db.todos
    todoscoll.delete_one({'completed': delstatus}) # delete data by task name

    return jsonify('Task Delete Sucefully')



@app.route('/getdataplaceholder', methods=['GET'])  # send a request to the API server and store the response. 
def request_response():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    todolist = json.loads(response.text)

    return todolist

@app.route('/adddataplaceholder', methods=['GET'])  # send a request to the API and add data in mongodb from jsonplaceholder

def add_data_placeholder():
    mycoll = mongo.db.todos
    url = requests.get('https://jsonplaceholder.typicode.com/todos/21')
    todoslist = json.loads(url.text)
    mycoll.insert_one(todoslist)

    return todoslist



if __name__ == '__main__':
    app.run(debug=True)