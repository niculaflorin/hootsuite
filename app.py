import json
from flask import Flask, request, render_template
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient()
db = client.test

@app.route('/')
def index():
	return render_template('add.html')

@app.route('/transactions', methods=['POST'])
def trans1():
	transactions = {
		'sender' : request.form['sender'],
		'receiver' : request.form['receiver'],
		'timestamp' : request.form['timestamp'],
		'suma' : request.form['suma']
	}
	db.test.insert_one(transactions)
	return 'Succesful insert'

@app.route('/transactions', methods=['GET'])
def trans2():
	user =  request.args.get('user')
	userInt = int(user)
	day =  request.args.get('day')
	dayInt = int(day)
	threshold = request.args.get('threshold')
	thresholdInt = int(threshold)

	cursor = db.test.find( { 
			 "$and" : [ 
				{ "$or" : [ { sender : { "$eq" : userInt} }, {receiver : { "$eq" : userInt} } ] },
				{timestamp : { "$eq" : dayInt}},
				{suma : { "$gt" : thresholdInt} }
			]
		})
	
	for result in cursor:
		print(result)

	
@app.route('/balance', methods=['GET'])
def balance():
	user =  request.args.get('user')
	userInt = int(user)
	start =  request.args.get('since')
	startInt = int(start)
	end = request.args.get('until')
	endInt = int(end)
	bal = 0	
	print bal
	while(startInt <= endInt):
		cursor = db.test.find({
			"$and" : [
				{ "$or" : [ { sender : { "$eq" : userInt} }, {receiver : { "$eq" : userInt} } ] },
				{timestamp : { "$eq" : startInt}},			
			]	
		})
		startInt += 1
		for result in cursor:
			value = json.load(result)
			bal += value['suma']
	print bal		

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
