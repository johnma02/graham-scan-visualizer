from flask import Flask, request, send_from_directory, redirect, url_for, send_file
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin 
from convexhull import graham_scan, Animator
from pymongo import MongoClient
import json
import sys
import numpy as np

app = Flask(__name__, static_url_path='/', static_folder='frontend/build')
CORS(app)
api = Api(app)

#mongoClient = MongoClient('mongodb://127.0.0.1:27017')
mongoClient = MongoClient('mongodb:27017', username="root", password="rootpassword")
db = mongoClient.get_database('submissions_db')
submissions_col = db.get_collection('submissions_col')
 

def update_gif(id):
    if submissions_col.find({"_id":id}):
        pts = list(map(lambda x : int(x), submissions_col.find_one({"_id":id})['vals'].split()))
    
        cartesian = []

        i = 0
        while(i < len(pts)):
            cartesian += [[pts[i], pts[i+1]]]
            i+=2
        processed_pts = graham_scan(np.unique(np.array(cartesian), axis=0))
        create_gif = Animator(processed_pts)
        create_gif.animate()
        return 

@app.route('/api/addsubmission', methods=['POST'])
def addsubmission():
    data = request.get_json()

    sub = data['vals']
    
    result = submissions_col.insert_one({"vals": sub})
    update_gif(result.inserted_id)

    return send_file("gscan.gif", mimetype="image/gif")
  # Save the item to the database

@app.route("/profile")
def app_profile():
    return {"Systems": "Nominal"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)
    
    
