from flask import Flask, render_template, request, redirect, jsonify 
import os
import pymongo
from pymongo import MongoClient


app = Flask(__name__)

# heroku_55k7w1dv

MONGO_URL = os.environ.get('MONGODB_URI') 
client = MongoClient(MONGO_URL)
db = client.heroku_55k7w1dv
collection = db.TEST


@app.route("/", methods=['GET']) 
def index(): 

	shouts = collection.find()
	return render_template('index.html', shouts=shouts)

# @app.route("/post", methods=['POST']) 
# def post(): 
# 	shout = {"name":request.form['name'], "message":request.form['message']} 
# 	shout_id = collection.insert(shout) 
# 	return redirect('/')

@app.route("/deleteAll", methods=['GET']) 
def deleteAll(): 
	collection.remove()
	return redirect('/')

@app.route("/changeStatus", methods=['POST']) 
def post(): 
	# shout = {"status":request.form['status'], "adress":"", "name":""} 
	find = { "neighborhood": request.form['colonia'] }
	values = { "$set": {
	      "neighborhood": request.form['colonia'],
	      "status": request.form['status'],
	      "address":"", "name":""
	      } }

	shout_id = collection.update_one(find,values) 
	return redirect('/')

@app.route("/createNew", methods=['POST']) 
def createNew(): 
	shout = {"neighborhood":request.form['colonia'],"status":0, "adress":"", "name":""}
	shout_id = collection.insert(shout)
	return redirect('/')

@app.route("/getStatus", methods=['GET']) 
def getStatus(): 
	jstatus = dict()
	find = {"neighborhood":request.args.get('colonia')}
	status = collection.find_one(find)
	jstatus = {'status':int(status['status']), 'address':status['address'], 'name':status['name']}
	return jsonify(jstatus)
	
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000)) 
	app.run(host='0.0.0.0', port=port)