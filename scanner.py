from bs4 import BeautifulSoup
from textprocessing import tokenizer, extract_text, extract_important, word_count
from posting import Posting

import os
import json


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
		with open(doc, encoding='utf-8', errors='replace') as json_file:
			if ".DS_Store" not in doc:
				print(doc)
				data = json.load(json_file)

				text = extract_text(data)
				
				tokens = tokenizer(text)
				important = tokenizer(extract_important(data))

				for token, frequency in tokens.items():
					if indexes.get(token, None) == None:
						indexes[token] = []
					p = Posting(n, frequency, token in important, word_count(text))
					indexes[token].append(p)

	return indexes

def get_in_dir(dirname):
	documents = []
	for file in os.listdir(dirname):
		path = os.path.join(dirname, file)
		if os.path.isdir(path):
			get_in_dir(path)
		elif os.path.isfile(path):
			documents.append(path)
	return documents
	
def get_files(main_dir) -> list:
	all_documents = []
	for file in os.listdir(main_dir):
		path = os.path.join(main_dir, file)
		if os.path.isdir(path):
			all_documents += get_in_dir(path)
		elif os.path.isfile(path):
			all_documents.append(path)
	return all_documents

	

if __name__ == '__main__':
	file_location = "ANALYST"
	build_index(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location)))

