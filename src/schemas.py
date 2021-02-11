from typing import List, Optional, Any, Dict, AnyStr, Union
from pydantic import BaseModel

#Define Request Schemas

class Transaction(BaseModel):
	'''Defines a transaction datapoint'''
	user: str
	item: str
	rating: Optional[int] = 0
	
TransactionsList = List[Transaction]

#Define Response Schemas