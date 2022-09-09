from flask import Flask, request, jsonify
from flask_cors import CORS
from route.repository import getAllBooks, addBook, removeBook, updateBook, getSingleBook
import json
import helpers.util as util

DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)

#enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/books', methods=['GET', 'POST'])
def books():
        response_object = {'status': 'FAILURE'}
        if request.method == 'GET':
                return json.dumps(getAllBooks(), default=util.obj_dict)
        if request.method == 'POST':
                post_data = request.get_json()
                print(post_data.get('name'))
                if addBook(post_data):
                        response_object = {'status': 'SUCCESS'}
        return jsonify(response_object)

@app.route('/books/<id>', methods=['PUT', 'DELETE', 'GET'])
def single_book(id):
        response_object = {'status': 'FAILURE'}
        if request.method == 'GET':
                return json.dumps(getSingleBook(id), default=util.obj_dict)
        if request.method == 'DELETE':
                if removeBook(id):
                        response_object = {'status': 'SUCCESS'}
        if request.method == 'PUT':
                if updateBook(request.get_json(), id):
                        response_object = {'status': 'SUCCESS'}
        return jsonify(response_object)

if __name__ == '__main__':
    app.run()
