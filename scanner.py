from bs4 import BeautifulSoup
from textprocessing import tokenizer, extract_text, extract_important 

import os
import json
import 

def scan_documents():
    simhashes = set() #simhash object
    tokens = dict() #key = word, value = number of instances
    pagecount = 0
    longest = ['', 0]


def build_index(Documents):
	indexes = dict()
	n = 0
	batch = 100
	for doc in Documents:
		n += 1

		with open(doc) as json_file:
			data = json.load(json_file)

			tokens = tokenizer(extract_text(data))
			important = tokenizer(extract_important(data))

		for token, frequency in tokens.items():
			if indexes.get(token, None) == None:
				indexes[token] = []
			p = Posting(n, frequency, token in important)
			indexes[token].append(p)

	return indexes

	
def get_files(main_dir) -> list:
	documents = []
	for file in os.listdir(main_dir):
		path = os.path.join(main_dir, file)
		if os.path.isdir(path):
			get_files(path)
		elif os.path.isfile(path):
			documents.append(path)
	return documents

	

if __name__ == '__main__':
	file_location = "ANALYST"
	build_index(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location)))

