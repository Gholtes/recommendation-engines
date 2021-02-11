from tinydb import TinyDB, Query

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

		#cache users and items to increase speed to check existance of a user, item
		self.user_cache = set()
		self.item_cache = set()

		self.update_cache()

	def get_users(self):
		return [i["id"] for i in self.users.all()]

	def get_users(self):
		return [i["id"] for i in self.items.all()]
	
	def add_transaction(self, transaction):
		self.transactions.insert(transaction)

		#update user and item stores if needed
		if not is_user(transaction["user"]):
			self.users.insert({"id": transaction["user"]})

		if not is_item(transaction["item"]):
			self.items.insert({"id": transaction["item"]})
		
		return transaction

	def update_cache(self):
		#dump DBs
		users = [i["id"] for i in self.users.all()]
		items = [i["id"] for i in self.items.all()]
		#Add to cache 
		for user in users:
			self.user_cache.add(user)
		for item in items:
			self.user_cache.add(item)
		pass

	def is_user(self, user):
		return user in self.user_cache

	def is_item(self, item):
		return item in self.item_cache