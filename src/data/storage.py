import tinydb

class reccomendationDB:
	def __init__(self):
		self.transactions = TinyDB('transactions.json')
		self.users = TinyDB('users.json')
		self.items = TinyDB('items.json')

		#cache users and items to increase speed to check existance of a user, item
		self.user_cache = set()
		self.item_cache = set()

		self.update_cache()
	
	def add_transaction(self, transaction):
		self.transactions.insert(transaction)
		if 

	def update_cache(self):
		pass

	def is_user(self, user):
		return user in self.user_cache

	def is_item(self, item):
		return item in self.item_cache