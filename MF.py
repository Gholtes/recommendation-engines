import numpy as np

class MF():
	'''
	Matrix Factorisation alogrithm based on Simon Funk's method
	Key input is the sparse user-item ratings array, with user ratings in an array with
	a row per user, and a column per item. Values are the users known rating, or zero if 
	no rating is available. 

	The output is a user-item ratings array with all items given a rating. The predicted raings can be 
	extracted from this array.
	'''
	def __init__(self, latent_features = 3, alpha = 0.0002, beta = 0.02, bias = False):
		self.latent_features = latent_features
		self.alpha = alpha
		self.beta = beta
		self.R_est = None
		self.H = None
		self.W = None
		self.R = None

		self.bias = bias
		self.user_bias = None
		self.item_bias = None
		
	def fit(self, R, iter = 10000, error_threshold = 0.005):
		self.R = R
		self.users, self.items = R.shape
		self.H = np.random.rand(self.users, self.latent_features)
		self.W = np.random.rand(self.latent_features, self.items)

		if self.bias:
			self.user_bias = np.random.rand(self.users, 1)
			self.item_bias = np.random.rand(1, self.items)

		for i in range(iter):
			# get Error:
			R_est = self._R_est()
			error = np.subtract(self.R, R_est)
			
			#Check for good match before max iter is reached			
			if self._error() < error_threshold:
				print("Local minima found after {0} iterations".format(i))
				break
			
			#Perform Gradient Decent
			for user in range(self.users):
				for item in range(self.items):
					if self.R[user,item] > 0: #Only use data where we have obvs
						e = error[user, item]

						for k in range(self.latent_features):
							self.H[user,k] += self.alpha * (2 * e * self.W[k,item] - self.beta * self.H[user, k])
							self.W[k,item] += self.alpha * (2 * e * self.H[user,k] - self.beta * self.W[k, item])
						
						if self.bias:
							self.item_bias[0, item] += self.alpha * (e - self.beta * self.item_bias[0, item])
							self.user_bias[user, 0] += self.alpha * (e - self.beta * self.user_bias[user, 0])
		
		self.R_est = np.matmul(self.H, self.W)
		return self._R_est()

	def _error(self):
		sum_error = 0
		error = np.subtract(self.R, self._R_est())
		for user in range(self.users):
			for item in range(self.items):
				if self.R[user,item] > 0:
					sum_error += abs(error[user, item])
		
		prop_error = sum_error / np.sum(self.R)	
		return prop_error
	
	def _R_est(self):
		if self.bias:
			return np.matmul(self.H, self.W) + self.user_bias + self.item_bias
		else:
			return np.matmul(self.H, self.W)

if __name__ == "__main__":
	#ratings array
	R = np.array([	[1, 0, 0, 4, 5],
					[2, 5, 1, 5, 5],
					[1, 4, 1, 5, 4],
					[4, 1, 4, 0, 3]])

	mf = MF(bias=True)
	R_est = mf.fit(R, error_threshold=0.005)

	print(R_est)
