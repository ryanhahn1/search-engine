import os
import json
from linecache import getline
import math

# scans the index and writes a file with dictionary of alphabet index
# def build_index_index(index_path):
# 	file_name = os.path.dirname(os.getcwd()) + "/index/alphabet.json"
# 	with open(index_path) as index:
# 		current = 0
# 		indexindex = dict() # key = alphanumeric char, value = int (line number)
# 		for line in iter(index.readline, ''):
# 			if line[0] != current:
# 				indexindex[line[0]] = index.tell()
# 				current = line[0]
# 		indexindex["last"] = index.tell()
# 	#print(indexindex)
# 	with open(file_name, 'w') as II_file:
# 		json.dump(indexindex, II_file)
# 	print("generated file")


def build_index_index(index_path):
	file_name = os.path.dirname(os.getcwd()) + "/index/alphabet.json"
	with open(index_path) as index:
		indexindex = dict() # key = word, value = seek (line number)
		pos = 0
		for line in iter(index.readline, ''):
			word = line.split(" ", 1)[0]
			print(word)
			indexindex[word] = pos
			pos = index.tell()
	#print(indexindex)
	with open(file_name, 'w') as II_file:
		json.dump(indexindex, II_file)
	print("generated file")

def get_index_index():
	alpha_path = os.path.dirname(os.getcwd()) + "/index/alphabet.json"
	with open(alpha_path) as alpha:
		index_index = json.load(alpha)
	return index_index

def get_url_index():
	url_index_file = os.path.dirname(os.getcwd()) + "/index/url_index.json"
	with open(url_index_file) as json_file:
		url_index = json.load(json_file)
	return url_index

# finds and returns the dictionary for the token, or None if it is not found
# def find_postings(token, index_path, indexindex):
# 	next_pos = indexindex[token[0]]

# 	# next_pos = when the iteration should end (next letter)
# 	if token[0] == "0":
# 		seek_pos = 0
# 	elif token[0] == "a":
# 		seek_pos = indexindex["9"]
# 	else:
# 		seek_pos = indexindex[chr(ord(token[0]) - 1)]
# 	print("finding: ", token)
# 	with open(index_path, "r") as index:
# 		index.seek(next_pos)
# 		for line in iter(index.readline, ''):
# 			word = line.split(" ", 1)[0]
# 			#print(word)
# 			if word == token:
# 				list_str = line.split(" ", 1)[1]
# 				#print(json.loads(list_str))
# 				return json.loads(list_str)
# 			elif index.tell() == next_pos:
# 				break
# 	print("token not in index")
# 	return None

def find_postings(token, index_path, indexindex):
	next_pos = indexindex[token]

	#print("finding: ", token)
	with open(index_path, "r") as index:
		index.seek(next_pos)
		line = index.readline()
		word = line.split(" ", 1)[0]
		print(word)
		list_str = line.split(" ", 1)[1]
		if word == token:
			return json.loads(list_str)
	print("token not in index")
	return None

# return a dictionary of the docID and the score
def find_all_boolean(query, index_path, index_index):
	words = dict() # key = token, value = list of postings, postings = dictionary
	all_posts = dict() # key = docID, value = number of instances
	good_posts = dict() # key = docID, value = summed score

	# adds every posting for all postings to all_posts
	for token in query.split():
		postings = find_postings(token, index_path, index_index)
		words[token] = postings
		print("found all postings")
		for post in postings:
			# assign or increment the number of times post is seen
			id = post["docID"]
			if id in all_posts:
				all_posts[id] += 1
				# add to good_posts if the post is seen enough times
				if all_posts[id] == len(query.split()):
					good_posts[id] = 0
			else:
				all_posts[id] = 1
	print("found all boolean results")
	for key, value in good_posts.items():
		good_posts[key] = sum_score(query, key, words)

	print("number of docs with all words:", len(good_posts))
	return good_posts
	
def sum_score(query, id, words):
	current_score = 0
	for token2 in query.split():
		current_score += [p["score"] for p in words[token2] if p["docID"] == id][0]
	return current_score

# total_with_term = length of postings list for that word
def get_tfidf(post, total_docs, total_with_term): 
	return ( (1 + math.log(post["term_freq"]) / post["word_count"]) / math.log( total_docs / total_with_term ) )

def score(post, total_docs, total_with_term):
	if post["importance"]:
		# adjust coefficient
		return 2 * get_tfidf(post, total_docs, total_with_term)
	else:
		return get_tfidf(post, total_docs, total_with_term)

def build_scores(path):
	new_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	scored = open(new_path, 'w')
	index = open(path, "r")
	for line in index:
		word, list_str = line.split(" ", 1)
		#print(word)
		list_real = json.loads(list_str)
		for post in list_real:
			post["score"] = score(post, 55393, len(list_real))
		s = word + " " + json.dumps(list_real) + "\n"
		scored.write(s)



if __name__ == '__main__':
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	not_path = os.path.dirname(os.getcwd()) + "/index/0.txt"
	build_index_index(main_path)
	#get_index_index(main_path)
	#find_postings("machine", main_path)
	#find_all_boolean("zot machine learning", main_path)
	#build_scores(main_path)
	#find_postings("machine", main_path)