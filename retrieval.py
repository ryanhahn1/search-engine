import os
import json
from linecache import getline
import math

# scans the index and returns a dictionary with positions of letter changes
def get_index_index(index_path):
	with open(index_path) as index:
		current = 0
		count = 0
		indexindex = dict() # key = alphanumeric char, value = int (line number)
		for line in index:
			if line[0] != current:
				indexindex[ line[0] ] = count
				count += 1
			else:
				count += 1
		indexindex["last"] = count
	#print(indexindex)
	return indexindex

# finds and returns the dictionary for the token, or None if it is not found
def find_postings(token, index_path):
	indexindex = get_index_index(index_path)
	next_pos = indexindex[token[0]]

	# next_pos = when the iteration should end (next letter)
	if token[0] == "0":
		seek_pos = 1
	elif token[0] == "a":
		seek_pos = indexindex["9"]
	else:
		seek_pos = indexindex[chr(ord(token[0]) - 1)]

	while seek_pos <= next_pos:
		word, list_str = getline(index_path, seek_pos).split(" ", 1)
		#print(word)
		if word == token:
			#print(json.loads(list_str))
			return json.loads(list_str)
		else:
			seek_pos += 1
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
	#print(len(query.split()))
	for key, value in all_posts.items():
		# add postings with all words to good_posts
		if value == len(query.split()):
			#print("good")
			good_posts[key] = 0
		else:
			#print("bad")
			pass
	
	# change good_postings value to be the score
	for key, value in good_posts.items():
		current_score = 0
		# sum the token scores for each doc
		for token in query.split():
			if [p for p in words[token] if p["docID"] == key]:
				#print(token, [p for p in words[token] if p["docID"] == key][0]["docID"])
				current_score += score([p for p in words[token] if p["docID"] == key][0], 55393, len(words[token]))
		good_posts[key] = current_score
	print(good_posts)
	


# total_with_term = length of postings list for that word
def get_tfidf(post, total_docs, total_with_term): 
	return ( (post["term_freq"] / post["word_count"]) / math.log( total_docs / total_with_term ) )

def score(post, total_docs, total_with_term):
	if post["importance"]:
		# adjust coefficient
		return 1.5 * get_tfidf(post, total_docs, total_with_term)
	else:
		return get_tfidf(post, total_docs, total_with_term)

if __name__ == '__main__':
	main_path = os.path.dirname(os.getcwd()) + "/index/0.txt"
	#get_index_index(main_path)
	#find_postings("zoo research", main_path)
	find_all_boolean("machine yes", main_path)