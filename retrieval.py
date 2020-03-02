import os
import json
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

def get_threshold_index():
	threshold_index_file = os.path.dirname(os.getcwd()) + "/index/threshold.json"
	with open(threshold_index_file) as threshold:
		threshold_index = json.load(threshold)
	return threshold_index

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
	if token in indexindex:
		next_pos = indexindex[token]


		#print("finding: ", token)
		with open(index_path, "r") as index:
			index.seek(next_pos)
			line = index.readline()
			#print(line)
			word = line.split(" ", 1)[0]
			#print(word)
			list_str = line.split(" ", 1)[1]
			if word == token:
				#print(json.loads(list_str))
			#	print(json.loads(list_str)[:5000])
				return json.loads(list_str)
	#print("token not in index")
	return None

# return a dictionary of the docID and the score
def find_all_boolean(q, index_path, index_index, threshold):
	words = dict() # key = token, value = list of postings, postings = dictionary
	all_posts = dict() # key = docID, value = number of instances
	good_posts = dict() # key = docID, value = summed score
	query, restrict = query_processing(q, threshold)


	if len(query) == 1:
		token = query[0]
		postings = find_postings(token, index_path, index_index)
		#print("found all postings")
		words[token] = postings
		#print(postings)
		if postings:
			#print(postings)
			if restrict:
					postings = postings[:500]
			for post in postings:
				good_posts[post["docID"]] = 0
		else:
			return None
	else:
		# adds every posting for all postings to all_posts
		for token in query:
			postings = find_postings(token, index_path, index_index)
			words[token] = postings
			#print("found all postings")
			if postings:
				if restrict:
					postings = postings[:500]
				for post in postings:
					# assign or increment the number of times post is seen
					id = post["docID"]
					#print(id)
					if id in all_posts:
						all_posts[id] += 1
						# add to good_posts if the post is seen enough times
						if all_posts[id] == len(query):
							good_posts[id] = 0
					else:
						all_posts[id] = 1
			else:
				return None
	#print("found all boolean results")
	for key, value in good_posts.items():
		good_posts[key] = sum_score(query, key, words)

	#print("number of docs with all words:", len(good_posts))
	return good_posts
	
def sum_score(query, id, words):
	# compute score for query
	# (score_query * score_document) / length?_d

	current_score = 0
	for token in query:
		current_score += [p["score"] for p in words[token] if p["docID"] == id][0]
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

def query_processing(s, threshold):
	stop_words = {'been', 'ours', "they're", 'when', 'into', '}', 'each', 'having', 'very', 'himself', 'between', 'they', 'this', "won't", '{', 'it', ',', "here's", 'not', "she's", 'am', "let's", 'other', 'under', "he'd", 'both', '^', 'if', 'he', 'themselves', '*', 'an', 'why', '!', "what's", 'but', 'doing', 'because', ';', 'of', "you'll", "there's", "it's", 'these', '/', 'for', "shouldn't", 'above', 'did', 'had', "isn't", 'she', 'through', "who's", "wouldn't", 'no', "you're", '-', 'down', 'a', "he'll", 'him', 'ought', "he's", '$', 'their', '||', 'on', 'as', "why's", '~', 'herself', 'than', 'his', "shan't", "she'll", 'hers', 'who', 'does', 'what', "when's", '<', '|', "haven't", 'yourselves', "you'd", '_', 'during', 'over', 'has', 'i', "where's", 'would', 'your', 'that', "didn't", '.', 'further', 'you', "you've", 'are', 'about', 'and', 'few', 'in', 'which', '"', '[', 'own', "they'd", 'its', 'while', 'or', 'ourselves', '@', "i've", 'most', "that's", 'below', 'do', '=', "can't", 'should', 'some', 'to', 'once', "aren't", ')', 'all', "she'd", 'more', 'we', 'where', ':', "wasn't", 'cannot', '\\', 'our', 'could', 'up', "we're", 'by', 'against', 'her', 'them', "we've", "couldn't", '#', 'any', "i'd", 'then', 'too', 'were', 'after', 'my', "weren't", 'until', 'whom', 'from', 'nor', "we'd", '`', 'itself', "i'm", 'so', "they've", "don't", "hasn't", 'same', '+', "i'll", 'have', '%', '?', 'is', 'myself', "doesn't", 'off', 'again', 'theirs', 'yourself', 'here', 'the', 'was', 'those', 'yours', 'such', 'at', "hadn't", "we'll", ']', 'only', 'being', "how's", 'me', 'out', '>', "mustn't", 'before', 'be', "they'll", 'with', '&', '(', 'how', 'there'}
	threshold_index = threshold
	restrict = True
	new_query = []
	old_query = s.split()
	for word in old_query:
		if word not in stop_words:
			if word in threshold_index and threshold_index[word] < 100:
				restrict = False
			new_query.append(word)
	if len(new_query) == 0:
		return (old_query, restrict)
	else:
		return (new_query, restrict)	

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

def build_ranked(path):
	new_path = os.path.dirname(os.getcwd()) + "/index/ranked.txt"
	scored = open(new_path, 'w')
	index = open(path, "r")
	for line in index:
		word, list_str = line.split(" ", 1)
		print(word)
		list_real = json.loads(list_str)
		list_real = sorted(list_real, key = lambda x: -x["score"])
		s = word + " " + json.dumps(list_real) + "\n"
		scored.write(s)
	index.close()
	scored.close()

def build_threshold():
	new_path = os.path.dirname(os.getcwd()) + "/index/threshold.json"
	index = open(os.path.dirname(os.getcwd()) + "/index/main.txt", "r")
	threshold = dict()
	with open(new_path, "w") as threshold_index:
		for line in index:
			word, list_str = line.split(" ", 1)
			print(word)
			list_real = json.loads(list_str)
			print(len(list_real))
			threshold[word] = len(list_real)
		json.dump(threshold, threshold_index)
	index.close()

if __name__ == '__main__':
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	#not_path = os.path.dirname(os.getcwd()) + "/index/0.txt"
	#indexindex = get_index_index()
	#threshold_index = get_threshold_index()
	#build_threshold()
	#build_ranked(main_path)
	#urlindex = get_url_index()
	#build_index_index(main_path)
	#get_index_index(main_path)
	#find_postings("zot", main_path, indexindex)
	find_all_boolean("machine learning", main_path, indexindex, threshold_index)
	#build_scores(main_path)