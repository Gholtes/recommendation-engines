
import numpy as np

class prod2prod():
	'''
	Naaive approch to product to product reccomendations
	1) Store reviews for each product by customer
	2) for each customer, find similar customers. Similar defiend as low cosine distance between product reviews.
	3) for each customer, find the top ranked products that they have not consumered, but similar customers have
	'''
	def __init__(self, R, promotion_threshold = 4):
		self.R = R
		self.customer_count, self.product_count = R.shape
		self.promotion_threshold = promotion_threshold

	def get(self, index):
		dist_scores = self.dist(self.R[index,:], self.R)
		ranked_users = sorted(zip(dist_scores, list(range(self.customer_count))))[1:]

		reccomendation_scores = np.zeros(self.product_count)
		for dist_score, user_index in ranked_users:
			if dist_score < max(dist_scores)/2:
				for product_id in range(self.product_count):
					if self.R[user_index, product_id] >= self.promotion_threshold and self.R[index, product_id] == 0:
						reccomendation_scores[product_id] += 1
		
		reccomendation_scores = reccomendation_scores/np.max(reccomendation_scores)
		return reccomendation_scores

	def dist(self, vector, vector_set):
		return np.sum(np.square(np.subtract(vector_set, vector)), axis = 1)
	
	def dist_matrix(self, matrix):
		np.apply_along_axis(self.dist, 1, matrix, matrix)

if __name__ == "__main__":
	R = np.array([	[1, 0, 0, 4, 5],
					[2, 5, 1, 5, 5],
					[1, 4, 1, 5, 4],
					[4, 1, 4, 0, 3],
					[5, 1, 0, 0, 0]])

	rec = prod2prod(R, promotion_threshold = 3)
