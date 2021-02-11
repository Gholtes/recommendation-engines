import requests
import os,sys,inspect
#Hacky 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from src.models.MF import MF
from src.data.pipeline import transaction2matrix

def openNetflixData(path, max_rows = 10000):
	with open(path, "r") as f:
		#Read file line by line, adding each line as a transacation
		line = f.readline()
		item = None #hold item in mem 
		transactions = []
		cnt = 1

		while line and cnt <= max_rows:
			line = line.strip()
			if ":" in line:
				item = line.split(":")[0]
			else:
				parsed_line = line.split(",")
				user = parsed_line[0]
				rating = parsed_line[1]

				transactions.append({"user":user, "item":item, "rating":rating}) #store transaction
			line = f.readline()
			cnt += 1
	
	return transactions


if __name__ == "__main__":
	#Load data
	transactions = openNetflixData("tests/data/combined_data_3.txt", max_rows = 2000)
	print("Data loaded")
	
	R = transaction2matrix(transactions) #TODO get users, items
 
	mf = MF()
	mf.fit()

# if __name__ == "__main__":
# 	url = "http://0.0.0.0:5000"
# 	requests.get(url+"/purge") #Purge past data
	
# 	#Load data
# 	transactions = openNetflixData("tests/data/combined_data_3.txt", max_rows = 2000)
# 	print("Data loaded")

# 	#Add data to API in batches
# 	for i in range(0,len(transactions),50):
# 		print("Adding transactions: {0} to {1}".format(i,i+50))
# 		batch = transactions[i:i+50]
# 		requests.post(url+"/add", json = batch)

# 	#Train the model
# 	preds = requests.post(url+"/train", json = {"epochs":100})
# 	print(preds.text)
	
