from typing import List, Optional, Any, Dict, AnyStr, Union
from pydantic import BaseModel

#Define Request Schemas

class TransactionRequest(BaseModel):
	'''Defines a transaction datapoint'''
	user: str
	item: str
	rating: Optional[int] = 0
	
TransactionsListRequest = List[TransactionRequest]

class TrainRequest(BaseModel):
	'''Defines a train request'''
	epochs: Optional[int] = 1000
	bias: Optional[bool] = False

class UserRecommendationRequest(BaseModel):
	user: str
	count: Optional[int] = 100

#Define Response Schemas