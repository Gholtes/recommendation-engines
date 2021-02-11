import requests

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
	url = "http://0.0.0.0:5000"
	requests.get(url+"/purge") #Purge past data
	
	#Load data
	transactions = openNetflixData("tests/data/combined_data_3.txt", max_rows = 100)
	print("Data loaded")

	#Add data to API in batches
	for i in range(0,len(transactions),50):
		print("Adding transactions: {0} to {1}".format(i,i+50)
		batch = transactions[i:i+50]
		requests.post(url+"/add", json = batch)

	#Train the model
	preds = requests.post(url+"/train", json = {"epochs":10000})
	print(preds)
	
