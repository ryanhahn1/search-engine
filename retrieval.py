# scans the index and generates an index with positions of letter changes
def getIndexIndex:
	with open("index") as file:
		current = 0
		count = 0
		indexindex = dict() # key = alphanumeric char, value = int (line number)
		for line in file:
			if line[0] != current:
				indexindex[ line[0] ] = count
				count += 1
			else:
				count += 1
	return indexindex

def findIndex(token):
	indexindex = getIndexIndex("index")
	seek_position = indexindex[token[0]]
	
	while

def findTopBoolean(query):
	with open("index") as file:
		for x in query.split():
			