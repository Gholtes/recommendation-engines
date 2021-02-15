import numpy as np

class transaction2matrix():
	'''transfroms user-item level transactions into a sparse ratings matrix'''
	def __init__(self, transaction_list, users, items):
		item_cnt = len(items)
		user_cnt = len(users)

		#Map users, items to indicies in the array
		self.user_index = {user:index for user,index in zip(users, list(range(user_cnt)))}
		self.item_index = {item:index for item,index in zip(items, list(range(item_cnt)))}

		ratings_matrix = np.zeros((user_cnt, item_cnt), dtype=np.float32)

		#Add transactions to ratings array
		for transaction in transaction_list:
			ratings_matrix[self.user_index[transaction["user"]], self.item_index[transaction["item"]]] = transaction["rating"]

		self.matrix = ratings_matrix