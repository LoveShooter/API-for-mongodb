#api_for_mongodb.py
#CRUD RESTApi with using Flask

import pymongo
import requests
import json, bson
import random
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS


app = Flask(__name__)
CORS(app)   # This will enable CORS for all routes

title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

app.config['MONGO_DBNAME'] = 'to-do-lists' # Name of database on mongo
app.config["MONGO_URI"] = "mongodb+srv://sysadm:Ff121314@cluster0-gpxwq.mongodb.net/to-do-lists" #URI to Atlas cluster  + Auth Credentials

mongo = PyMongo(app)


@app.route('/getdata', methods=['GET'])  # Find all data in my collection
def get_all_data():
    todos = mongo.db.todos # Connect to my collection

    output = []

    for q in todos.find():   # q - like query
        output.append({'userId': q['userId'], 'id': q['id'], 'title': q['title'], 'completed': q['completed']})

    return jsonify({'result': output})



#@app.route('/getdata/<status>', methods=['GET'])
#def get_one_data(status):
#    todos = mongo.db.todos
#   q = todos.find_one({'completed': bool(status)}) # Find by status
#    if q:
#        output = {'completed': q[bool(status)], 'userId': q['userId'], 'id': q['id'], 'title': q['title']}
#    else:
#        output = 'No results found!'
#
#    return jsonify({'result': output})



@app.route('/adddata', methods=['POST']) # Add data in db. Need input JSON-like data.
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


@app.route('/deldata/<int:todo_id>', methods=['GET'])
def del_one_data(todo_id):
    todoscoll = mongo.db.todos
    todoscoll.delete_one({'id': todo_id}) # Delete data by todo ID

    return jsonify('Task deleted successfully!')



@app.route('/getdataplaceholder', methods=['GET'])  # Send a request to the API server and store the response. 
def request_response():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    todolist = json.loads(response.text)

    return todolist

@app.route('/adddataplaceholder', methods=['GET'])  # Send a request to the API and add data in mongodb from jsonplaceholder
def add_data_placeholder():
    mycoll = mongo.db.todos
    
    url1 = 'https://jsonplaceholder.typicode.com/todos/1'
    url2 = 'https://jsonplaceholder.typicode.com/todos/21'
    url3 = 'https://jsonplaceholder.typicode.com/todos/32'
    url4 = 'https://jsonplaceholder.typicode.com/todos/13'
    url5 = 'https://jsonplaceholder.typicode.com/todos/16'
    
    urls = [url1, url2, url3, url4, url5]

    url = requests.get(random.choice(urls))
    todoslist = json.loads(url.text)
    mycoll.insert_one(todoslist)
    
    return todoslist


if __name__ == '__main__':
    app.run(debug=True)