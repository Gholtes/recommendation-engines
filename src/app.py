'''
--------------------------------------------------
File: app.py
--------------------------------------------------
Author: Deloitte Australia 2021

Description: Defines the application that will provide the API for the reccomendation engines

Endpoints:
#TODO

Run with $ uvicorn src.app:app --reload --host 0.0.0.0 --port 5000
--------------------------------------------------
Edit History:

#  | NAME				|  DATE       	| DESC
0  | Grant Holtes       |  11/2/21		| Initial Creation 
--------------------------------------------------
'''
#FastAPI imports
from fastapi import FastAPI, Response, status
import traceback
#model and data pipeline imports
import numpy as np
import json
import os

#Reqest and Response Schemas
from src.schemas import *

#Model imports
from src.models.MF import MF

#import data items
from src.data.storage import reccomendationDB
from src.data.pipeline import transaction2matrix

#Config HTTP error codes
bad_input_code = 400
out_of_order_code = 400
general_app_error_code = 500

#Initialise key services
app = FastAPI()
db = reccomendationDB()

@app.get('/')
async def home():
    return {"app":"Reccomendation Engine API", "Created by": "Deloitte Australia"}

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
		#transform data
		ratings_matrix = transaction2matrix(db.get_transactions(), db.get_users(), db.get_items()).matrix
		#create and train model
		mf = MF()
		mf.fit(ratings_matrix, iter = request.epochs)
		print(mf.R_est)
		return {"status":"success"}
	
	except Exception as e:
        response.status_code = general_app_error_code
        return {"status":"error", "error": str(e), "traceback": str(traceback.format_exc())}



#Admin end-points
@app.get('/contents/', status_code=200)
def contents():
	'''Add a set of user transactions into the database'''
	items = db.get_items()
	users = db.get_users()
	return {"users":users, "items":items}

@app.get('/purge/', status_code=200)
def purge():
	'''Remove DB contents'''
	db._purgeDB()


    
'''
Example requests

curl --location --request POST 'http://0.0.0.0:5000/add' --header 'Content-Type: application/json' --data-raw '[{"user": 1, "item": 1, "rating": 1}]'


curl --location --request POST 'http://0.0.0.0:5000/train' --header 'Content-Type: application/json' --data-raw '{}'

'''