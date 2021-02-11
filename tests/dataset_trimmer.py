#makes a smaller dataset for testing

n = 20000

with open("tests/data/combined_data_3.txt", "r") as f:
	lines = f.readlines()
	print(len(lines))
	
with open("tests/data/combined_data_3_small.txt", "w") as f:
	for i in range(n):
		f.write(lines[i])
