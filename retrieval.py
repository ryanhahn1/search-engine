import os
import json
import math

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
					postings = postings[:2500]
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
					postings = postings[:2500]
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

if __name__ == '__main__':
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	#not_path = os.path.dirname(os.getcwd()) + "/index/0.txt"
	#indexindex = get_index_index()
	#threshold_index = get_threshold_index()
	#urlindex = get_url_index()
	#get_index_index(main_path)
	#find_postings("zot", main_path, indexindex)
	find_all_boolean("machine learning", main_path, indexindex, threshold_index)