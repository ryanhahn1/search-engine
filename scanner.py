from bs4 import BeautifulSoup
from textprocessing import tokenizer, extract_text, extract_important
from posting import create_posting

import os
import json
import re


def scan_documents():
    simhashes = set() #simhash object
    tokens = dict() #key = word, value = number of instances
    pagecount = 0
    longest = ['', 0]


def build_index(Documents):
	directory = os.path.dirname(os.getcwd()) + "/index/"
	indexes = dict()
	total_docs = 0
	batch_num = 0
	n = 0
	batch = 1

	for doc in Documents:
		batch += 1
		n += 1
		with open(doc, encoding='utf-8', errors='replace') as json_file:
			if ".DS_Store" not in doc:
				print(total_docs)
				total_docs += 1
				data = json.load(json_file)

				text = extract_text(data)
				important_text = extract_important(data)

				text = re.sub('[^a-z0-9]', ' ', text.lower()).split()
				important_text = re.sub('[^a-z0-9]', ' ', important_text.lower()).split()
				
				
				tokens = tokenizer(text)
				important = tokenizer(important_text)

				for token, frequency in tokens.items():
					if indexes.get(token, None) == None:
						indexes[token] = []
					p = create_posting(n, frequency, (token in important), len(text))
					indexes[token].append(p)
		if batch > 1000:
			s = ""
			for k,v in sorted(indexes.items()):
				s += k + " " + json.dumps(v) + "\n"
			file_name = str(batch_num)  + ".txt"
			with open(os.path.join(directory, file_name), 'w') as data_file:
				data_file.write(s)	
			del indexes
			indexes = dict()
			batch = 0
			batch_num += 1
	s = ""
	for k,v in sorted(indexes.items()):
		s += k + " " + json.dumps(v) + "\n"
	file_name = str(batch_num)  + ".txt"
	with open(os.path.join(directory, file_name), 'w') as data_file:
		data_file.write(s)	

	#print('total documents:', total_docs)
	#return indexes

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
	file_location = "analyst"
	build_index(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location)))
	#print(len(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location))))

