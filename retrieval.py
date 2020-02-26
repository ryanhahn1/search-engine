import os
import json
from linecache import getline
import math

# scans the index and writes a file with dictionary of alphabet index
def build_index_index(index_path):
	file_name = os.path.dirname(os.getcwd()) + "/index/alphabet.json"
	with open(index_path) as index:
		current = 0
		indexindex = dict() # key = alphanumeric char, value = int (line number)
		for line in iter(index.readline, ''):
			if line[0] != current:
				indexindex[line[0]] = index.tell()
				current = line[0]
		indexindex["last"] = index.tell()
	#print(indexindex)
	with open(file_name, 'w') as II_file:
		json.dump(indexindex, II_file)
	print("generated file")

def get_index_index():
	alpha_path = os.path.dirname(os.getcwd()) + "/index/alphabet.json"
	with open(alpha_path) as alpha:
		index_index = json.load(alpha)
	return index_index

# finds and returns the dictionary for the token, or None if it is not found
def find_postings(token, index_path):
	indexindex = get_index_index()
	next_pos = indexindex[token[0]]
	print("loaded indexindex")

	# next_pos = when the iteration should end (next letter)
	if token[0] == "0":
		seek_pos = 0
	elif token[0] == "a":
		seek_pos = indexindex["9"]
	else:
		seek_pos = indexindex[chr(ord(token[0]) - 1)]
	print("finding: ", token)
	with open(index_path, "r") as index:
		index.seek(next_pos)
		for line in iter(index.readline, ''):
			word, list_str = line.split(" ", 1)
			#print(word)
			if word == token:
				#print(json.loads(list_str))
				return json.loads(list_str)
			elif index.tell() == next_pos:
				break
	print("token not in index")
	return None

# return a dictionary of the docID and the score
def find_all_boolean(query, index_path):
	words = dict() # key = token, value = list of postings, postings = dictionary
	all_posts = dict() # key = docID, value = number of instances
	good_posts = dict() # key = docID, value = summed score

	# adds every posting for all postings to all_posts
	for token in query.split():
		postings = find_postings(token, index_path)
		words[token] = postings
		for post in postings:
			#print(post)
			if post["docID"] in all_posts:
				all_posts[post["docID"]] += 1
			else:
				all_posts[post["docID"]] = 1
	print("found all postings")
	#print(len(query.split()))
	for key, value in all_posts.items():
		# add postings with all words to good_posts
		if value == len(query.split()):
			#print("good")
			good_posts[key] = 0
		else:
			#print("bad")
			pass
	print("calculating scores")
	# change good_postings value to be the score
	print(len(good_posts))
	for key, value in good_posts.items():
		current_score = 0
		# sum the token scores for each doc
		for token in query.split():
			#print(token)
			post_list = [p for p in words[token] if p["docID"] == key]
			#print("created post_list")
			if post_list:
				#print(token, [p for p in words[token] if p["docID"] == key][0]["docID"])
				current_score += score(post_list[0], 55393, len(words[token]))
		good_posts[key] = current_score
	print("calculated scores")
	return good_posts
	


# total_with_term = length of postings list for that word
def get_tfidf(post, total_docs, total_with_term): 
	return ( (1 + math.log(post["term_freq"]) / post["word_count"]) / math.log( total_docs / total_with_term ) )

def score(post, total_docs, total_with_term):
	if post["importance"]:
		# adjust coefficient
		return 5 * get_tfidf(post, total_docs, total_with_term)
	else:
		return get_tfidf(post, total_docs, total_with_term)

if __name__ == '__main__':
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	build_index_index(main_path)
	#get_index_index(main_path)
	#find_postings("zot", main_path)
	find_all_boolean("zot machine learning", main_path)