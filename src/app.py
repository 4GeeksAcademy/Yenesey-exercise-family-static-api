"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jhon = {
    "first_name": "Jhon",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}
jane = {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

jimmy = {
    "first_name": "jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(jhon)
jackson_family.add_member(jane)
jackson_family.add_member(jimmy)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        
        "family": members
    }


    return jsonify(response_body), 200





@app.route('/members', methods=['POST'])
def add_new_member():

    request_body = request.json

    if not request_body:
       return jsonify({"error": "Invalid input"}), 400
    
    new_member = jackson_family.add_member(request_body)

    return jsonify(new_member), 200




@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):

    result = jackson_family.delete_member(id)    
    if "done" in result:
        return jsonify({"msg": "Member deleted"}), 200
    
    return jsonify({"Error": "Member not found"}), 404




@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):

    member = jackson_family.get_member(id)    

    if not member:
        return jsonify({"Error": "Member not found"}), 404
    
    response_body = {
        "Member": member
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
