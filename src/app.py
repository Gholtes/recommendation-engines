'''
--------------------------------------------------
File: app.py
--------------------------------------------------
Author: Deloitte Australia 2021

Description: Defines the application that will provide the API for the recommendation engines

Endpoints:
#TODO

Run with 
	$ uvicorn src.app:app --reload --host 0.0.0.0 --port 5000
Or build and run with
	$ export DOCKER_BUILDKIT=0
	$ docker image build -t recommendation-engine-app .
	$ docker run -p 5000:5000 --name re-app -d recommendation-engine-app
--------------------------------------------------
Edit History:

#  | NAME				|  DATE       	| DESC
0  | Grant Holtes       |  11/2/21		| Initial Creation 
--------------------------------------------------
'''
#FastAPI imports
from fastapi import FastAPI, Response, status, Form
from fastapi.responses import HTMLResponse
import traceback
#model and data pipeline imports
import numpy as np
import json
import os
import csv

#Reqest and Response Schemas
from src.schemas import *

#Model imports
from src.models.MF import MF

#import data items
from src.data.storage import recommendationDB
from src.data.pipeline import transaction2matrix

#Config HTTP error codes
bad_input_code = 400
out_of_order_code = 400
general_app_error_code = 500

#Initialise key services
app = FastAPI()
db = recommendationDB()

#On Startup
if db.get_users:  #if there is data, train the model
	MF_matrix = transaction2matrix(db.get_transactions(), db.get_users(), db.get_items())
	ratings_matrix = MF_matrix.matrix

	#create and train model
	mf = MF()
	mf.fit(ratings_matrix, iter = 500)


@app.get('/')
async def home():
	return {"app":"recommendation Engine API"}

@app.get('/health/', status_code = 204)
async def health():
	print("Health check")

#Core end-points
@app.post('/add/', status_code=200)
def add(request: TransactionsListRequest, response: Response):
	'''Add a set of user transactions into the database'''
	try:
		for transaction in request:
			db.add_transaction({"user": transaction.user, "item": transaction.item, "rating":transaction.rating})
		return {"status":"success"}
	
	except Exception as e:
		response.status_code = general_app_error_code
		return {"status":"error", "error": str(e), "traceback": str(traceback.format_exc())}

@app.post('/train/', status_code=200)
def train(request: TrainRequest, response: Response):
	'''Train / fit the model'''
	try:
		global MF_matrix
		global mf
		
		#transform data
		MF_matrix = transaction2matrix(db.get_transactions(), db.get_users(), db.get_items())
		ratings_matrix = MF_matrix.matrix
		
		#create and train model
		mf = MF()
		mf.fit(ratings_matrix, iter = request.epochs)
		
		return {"status":"success"}
	
	except Exception as e:
		response.status_code = general_app_error_code
		return {"status":"error", "error": str(e), "traceback": str(traceback.format_exc())}

@app.post('/recommend-user/', status_code=200)
def recommend_user(request: UserRecommendationRequest, response: Response):
	'''get recommended items'''
	try:
		user_to_index, item_to_index = MF_matrix.user_index, MF_matrix.item_index
		user = request.user
		if user not in user_to_index.keys():
			response.status_code = bad_input_code
			return {"status":"error", "error": "user not in database"}
		
		#Get reccomenations from mf model and
		#Extract user's recommendations
		predicted_item_ratings = mf.R_est[user_to_index[user], :]
		existing_item_ratigs = mf.R[user_to_index[user], :]

		recommendations = {}
		cnt = 1
		#Rank recommendations, and recommend the top items that the user hasnt rated yet. only return a max of request.count items
		for item_est, item_actual, index in sorted(zip(predicted_item_ratings, existing_item_ratigs, list(range(len(predicted_item_ratings)))), reverse=True):
			if item_actual == 0 and cnt <= request.count: #New product to user
				recommendations[index] = item_est
				cnt +=1
		
		return {"user":request.user, "recommendations":recommendations}


	except Exception as e:
		response.status_code = general_app_error_code
		return {"status":"error", "error": str(e), "traceback": str(traceback.format_exc())}


#Quick and dirty admin end-points
@app.get('/admin/', status_code=200)
def admin():
	html_content = """
	<html>
		<head>
			<title>Recommendation Engine Admin</title>
		</head>
		<body>
			<h1>Recommendation Engine Admin</h1>
			<h2>Info:</h2>
			<form action="/keys">
    			<input type="submit" value="Items and Users" />
			</form>
			<form action="/mf">
    			<input type="submit" value="MF model arrays" />
			</form>
			<h2>Model Actions:</h2>
			<form action="/train-admin">
    			<input type="submit" value="Train model" />
			</form>
			<h2>Data Actions:</h2>
			<form action="/load">
    			<input type="submit" value="Load dummy data" />
			</form>
			<form action="/purge">
    			<input type="submit" value="CLEAR DATABASE" />
			</form>

			<h2>Add Data:</h2>
			<form action="/add-admin/" method="post">
				<label for="user">User:</label><br>
				<input type="text" id="user" name="user"><br>
				<label for="item">Item:</label><br>
				<input type="text" id="item" name="item"><br>
				<label for="rating">Rating:</label><br>
				<input type="text" id="rating" name="rating"><br>
				<input type="submit" value="Add">
			</form>

			<h2>Get recommendation:</h2>
			<form action="/recc-admin/" method="post">
				<label for="user">User:</label><br>
				<input type="text" id="user" name="user"><br>
				<input type="submit" value="Get">
			</form>
		</body>
	</html>
	"""
	return HTMLResponse(content=html_content, status_code=200)

@app.get('/purge/', status_code=200)
def purge():
	'''Remove DB contents'''
	db._purgeDB()
	return {"status": "successful"}

@app.get('/keys/', status_code=200)
def keys():
	'''Add a set of user transactions into the database'''
	items = db.get_items()
	users = db.get_users()
	return {"users":users, "items":items}

@app.get('/mf/', status_code=200)
def mf_render():
	'''View MF arrays'''
	input_array = mf.R
	predicted_array = mf.R_est
	html_content = """
	<html>
		<head>
			<title>MF array viewer</title>
		</head>
		<body>
			<h1>MF Arrays</h1>
			<p>Input data</p>
	"""
	html_content += HTML_table(input_array)

	html_content += "<p>Output Array</p>"

	html_content += HTML_table(predicted_array)
	html_content +=		"""
		</body>
	</html>
	"""
	return HTMLResponse(content=html_content, status_code=200)

def HTML_table(array):
	html = ["""<table style="width:100%">"""]
	for row in array:
		html.append("\n")
		html.append("<tr>")
		for column in row:
			html.append("<th>"+str(round(column,2))+"</th>\n")
		html.append("</tr>\n")
	html.append("</table>")
	return "".join(html)

@app.get('/load/', status_code=200)
def load_dummy_data():
	with open("src/data/data/tiny.csv", "r") as f:
		reader = csv.reader(f)
		resp = {}
		i = 0
		for row in reader:
			db.add_transaction({"user": row[0], "item": row[1], "rating":row[2]})
			resp[i] = {"user": row[0], "item": row[1], "rating":row[2]}
			i += 1
	return resp

@app.post('/add-admin', status_code=200)
def add_admin(user: str = Form(...), item: str = Form(...), rating: str = Form(...)):
	print("Adding: user {0}, item {1}, rating {2}".format(user, item, rating))
	db.add_transaction({"user": user, "item": item, "rating": rating})
	return {"status":"success"}

@app.post('/recc-admin', status_code=200)
def recc_admin(user: str = Form(...)):
	request = UserRecommendationRequest
	request.user = user
	request.count = 100
	return recommend_user(request, response = Response)

@app.get('/train-admin/', status_code=200)
def train_admin(response: Response):
	'''Train / fit the model without input '''
	request = TrainRequest
	request.epochs = 2000
	return train(request, response = Response)
		
	
'''
Example requests

curl --location --request POST 'http://0.0.0.0:5000/add' --header 'Content-Type: application/json' --data-raw '[{"user": 1, "item": 1, "rating": 1}]'


curl --location --request POST 'http://0.0.0.0:5000/train' --header 'Content-Type: application/json' --data-raw '{}'

curl --location --request POST 'http://0.0.0.0:5000/recommend-user' --header 'Content-Type: application/json' --data-raw '{"user":1}'

'''