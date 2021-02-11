'''
--------------------------------------------------
File: app.py
--------------------------------------------------
Author: Deloitte Australia 2021

Description: Defines the application that will provide the API for the reccomendation engines

Endpoints:
#TODO

Run with $ uvicorn src.app:app --reload
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

#Config HTTP error codes
bad_input_code = 400
out_of_order_code = 400
general_app_error_code = 500

#App definition
app = FastAPI()

@app.get('/')
async def home():
    return {"app":"Reccomendation Engine API", "Created by": "Deloitte Australia"}

@app.get('/health/', status_code = 204)
async def health():
    print("Health check")

#Core end-points
@app.post('/add/', status_code=200)
def add(request: TransactionsList, response: Response):
	'''Add a set of user transactions into the database'''
	for transaction in request:
		pass

    
