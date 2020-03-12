from bs4 import BeautifulSoup
from textprocessing import tokenizer, extract_text, extract_important
from posting import create_posting
from simhash import Simhash
import os
import json
import re

# go through each document in batches, add the index created in each batch to a file
def build_index(Documents):
	directory = os.path.dirname(os.getcwd()) + "/index/"
	indexes = dict()
	simhash = set()
	total_docs = 0
	batch_num = 0
	n = 0
	batch = 1
	for doc in Documents:
		batch += 1
		n += 1
		with open(doc, encoding='utf-8', errors='replace') as json_file:
			if ".DS_Store" not in doc:
				total_docs += 1
				data = json.load(json_file)
				text = extract_text(data)
				important_text = extract_important(data)
				# NOT DUPLICATE
				if is_not_duplicate(text, simhash):
					# TOKENIZE AND ADD TO INDEX
					text = re.sub('[^a-z0-9]', ' ', text.lower()).split()
					important_text = re.sub('[^a-z0-9]', ' ', important_text.lower()).split()
					tokens = tokenizer(text)
					important = tokenizer(important_text)
					for token, frequency in tokens.items():
						if indexes.get(token, None) == None:
							indexes[token] = []
						p = create_posting(n, frequency, (token in important), len(text))
						indexes[token].append(p)
		# NEW BATCH, WRITE CURRENT INDEX TO FILE
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
	# LAST BATCH
	s = ""
	for k,v in sorted(indexes.items()):
		s += k + " " + json.dumps(v) + "\n"
	file_name = str(batch_num)  + ".txt"
	with open(os.path.join(directory, file_name), 'w') as data_file:
		data_file.write(s)	

# returns a list of all the files in a subfolder of DEV
def get_in_dir(dirname):
	documents = []
	for file in os.listdir(dirname):
		path = os.path.join(dirname, file)
		if os.path.isdir(path):
			get_in_dir(path)
		elif os.path.isfile(path):
			documents.append(path)
	return documents

# return a list of all the file paths in the DEV folder
def get_files(main_dir) -> list:
	all_documents = []
	for file in os.listdir(main_dir):
		path = os.path.join(main_dir, file)
		if os.path.isdir(path):
			all_documents += get_in_dir(path)
		elif os.path.isfile(path):
			all_documents.append(path)
	return all_documents

# generate a file with a dictionary: key = docID, value = url
def build_url_index(Documents):
	directory = os.path.dirname(os.getcwd()) + "/index/"
	n = 0
	url_index = dict()
	for doc in Documents:
		n += 1
		with open(doc, encoding='utf-8', errors='replace') as json_file:
			if ".DS_Store" not in doc:
				data = json.load(json_file)
				url_index[n] = data['url']
	file_name = os.path.join(directory, "url_index.json")
	with open(file_name, 'w') as url_file:
		json.dump(url_index, url_file)

# returns boolean for if the document is a near duplicate
def is_not_duplicate(text, simhashes):
	current_sim = Simhash(text)

	if len(simhashes) == 0:
		simhashes.add(current_sim)
		return True
	
	for x in simhashes:
		if current_sim.distance(x) <= 2:
			print("duplicate detected")
			return False
	simhashes.add(current_sim)
	return True


if __name__ == '__main__':
	file_location = "DEV"
	build_index(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location)))
	#build_url_index(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location)))
	#print(len(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location))))

