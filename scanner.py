import os

def scan_documents():
    simhashes = set() #simhash object
    tokens = dict() #key = word, value = number of instances
    pagecount = 0
    longest = ['', 0]


def buildIndex():
	indexes = dict()
	n = 0
	for doc in Documents:
		n += 1
		# Tokens = set(tokenize(doc)) Tokens is set of tokens
		for token in Tokens:
			if indexes.get(token, None) == None:
				indexes[token] = []
			# p = posting(n, frequency, bool)
			indexes[token].append(p)
	return indexes

	
def get_files(main_dir):
	for file in os.listdir(main_dir):
		path = os.path.join(main_dir, file)
		if os.path.isdir(path):
			get_files(path)
		elif os.path.isfile(path):
			print(file)


if __name__ == '__main__':
	file_location = "ANALYST"
	get_files(os.path.join(os.path.dirname(os.getcwd()), file_location))