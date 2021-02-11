import numpy as np

class transaction2matrix():
	'''transfroms user-item level transactions into a sparse ratings matrix'''
	def __init__(self, transaction_list, users, items):
		item_cnt = len(items)
		user_cnt = len(users)

		#Map users, items to indicies in the array
		user_index = {user:index for user,index in zip(users, list(range(user_cnt)))}
		item_index = {item:index for item,index in zip(items, list(range(item_cnt)))}

		ratings_matrix = np.empty((user_cnt, item_cnt), dtype=np.float32)

		#Add transactions to ratings array
		for transaction in transaction_list:
			ratings_matrix[user_index[transaction["user"]], item_index[transaction["item"]]] = transaction["rating"]

		self.matrix = ratings_matrix