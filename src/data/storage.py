from tinydb import TinyDB, Query
import os

class reccomendationDB:
	'''
	Data model to store reccomendation data. 
	Three key componants:
	1) Transactions:
		The interactions between users and items are stored as transactions
		structure: {"user": STR, "item": STR, "rating": INT}
		#TODO add further fields as needed
	
	2) Users:
		Users are the unique users from transactions. We also store user level data here, 
		such as contact details, known charicteristsics, categories
		structure: {id: user_id, ...other fields }
		#TODO add further fields as needed
	
	3) Items:
		Unique items from transactions and any item level data.
		structure: {id: item_id, ...other fields }
		#TODO add further fields as needed

	'''
	def __init__(self):
		self.transactions = TinyDB('src/data/data/transactions.json')
		self.users = TinyDB('src/data/data/users.json')
		self.items = TinyDB('src/data/data/items.json')
	
	def add_transaction(self, transaction):
		'''adds a transaction to the tables'''
		self.transactions.insert(transaction)

		#update user and item stores if needed
		if not self.is_user(transaction["user"]):
			self.users.insert({"id": transaction["user"]})

		if not self.is_item(transaction["item"]):
			self.items.insert({"id": transaction["item"]})

		return transaction
	
	def get_transactions(self):
		'''dumps all transactions'''
		return self.transactions.all()

	def get_users(self):
		return [i["id"] for i in self.users.all()]

	def get_items(self):
		return [i["id"] for i in self.items.all()]
	
	def is_user(self, user):
		return user in self.get_users()

	def is_item(self, item):
		return item in self.get_items()

	def _purgeDB(self):
		os.remove('src/data/data/transactions.json')
		os.remove('src/data/data/users.json')
		os.remove('src/data/data/items.json')

	