import os
import json
import math

# create a copy of the index but with the calculated tf-idf scores for each posting
def build_scores(path):
	print("generating ranked")
	new_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	scored = open(new_path, 'w')
	index = open(path, "r")
	for line in index:
		word, list_str = line.split(" ", 1)
		#print(word)
		list_real = json.loads(list_str)
		for post in list_real:
			post["score"] = score(post, 55393, len(list_real))
		list_real = sorted(list_real, key = lambda x: -x["score"])
		s = word + " " + json.dumps(list_real) + "\n"
		scored.write(s)
	index.close()
	scored.close()
	print("generated ranked")

# build a file of a dictionary: key = word, value = char position in index file
def build_index_index(index_path):
	print("generating indexindex")
	file_name = os.path.dirname(os.getcwd()) + "/index/alphabet.json"
	with open(index_path) as index:
		indexindex = dict() # key = word, value = seek (line number)
		pos = 0
		for line in iter(index.readline, ''):
			word = line.split(" ", 1)[0]
			indexindex[word] = pos
			pos = index.tell()
	with open(file_name, 'w') as II_file:
		json.dump(indexindex, II_file)
	print("generated indexindex")

# build a file of a dictionary: key = token, value = number of postings
def build_threshold():
	print("generating threshold")
	new_path = os.path.dirname(os.getcwd()) + "/index/threshold.json"
	index = open(os.path.dirname(os.getcwd()) + "/index/main.txt", "r")
	threshold = dict()
	with open(new_path, "w") as threshold_index:
		for line in index:
			word, list_str = line.split(" ", 1)
			list_real = json.loads(list_str)
			threshold[word] = len(list_real)
		json.dump(threshold, threshold_index)
	index.close()
	print("generated threshold")

def score(post, total_docs, total_with_term):
	return get_tfidf(post, total_docs, total_with_term)

# returns the tf-idf score for a posting
# total_with_term = length of postings list for that word
def get_tfidf(post, total_docs, total_with_term):
	tfidf = ( math.log(1 + (post["term_freq"])) * math.log( total_docs / total_with_term ) )
	return tfidf

if __name__ == '__main__':
	old_path = os.path.dirname(os.getcwd()) + "/index/old_main.txt"
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	build_scores(old_path)
	build_index_index(main_path)
	build_threshold()