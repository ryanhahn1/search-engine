import time 
import json
import os
import heapq
import math
from retrieval import find_postings, get_url_index, get_url_ranking
from textprocessing import query_processor


def sum_score(query, id, words, urlrank, urlindex, seen):
	importance_sum = 1
	url_sum = 1
	score_sum = 0
	token_length = 0
	score_length = 0
	boolean_sum = 1
	page_score = 1

	#set page rank score
	if str(id) in urlrank:
		page_score = (1 + urlrank[str(id)] * 1000)
	
	
	for token in query:
		if token in words:
			p = [p for p in words[token] if p["docID"] == id]
			if len(p) >= 1:
				#check if this word is important in this document
				if p[0]["importance"]:
					importance_sum = importance_sum * 1.1
				#check if the url for this doc has the token in it
				if token in urlindex[str(id)].lower():
					#print("TOKEN IN URL", urlindex[str(id)])
					url_sum = url_sum * 1.1
				if seen[id] == len(query):
					boolean_sum = boolean_sum * 1000
				# find the vectors for document and token
				doc_score = p[0]["score"]
				token_score = query.count(token) * (55393 / len(words[token]))
				#token_score = 1
				# add the vectors to the sums
				token_length += token_score ** 2
				score_length += doc_score ** 2
				score_sum += doc_score * token_score

	
	return page_score * url_sum * importance_sum * boolean_sum * (score_sum / math.sqrt(token_length * score_length))

def query_processing(s):
	stop_words = {'been', 'ours', "they're", 'when', 'into', '}', 'each', 'having', 'very', 'himself', 'between', 'they', 'this', "won't", '{', 'it', ',', "here's", 'not', "she's", 'am', "let's", 'other', 'under', "he'd", 'both', '^', 'if', 'he', 'themselves', '*', 'an', 'why', '!', "what's", 'but', 'doing', 'because', ';', 'of', "you'll", "there's", "it's", 'these', '/', 'for', "shouldn't", 'above', 'did', 'had', "isn't", 'she', 'through', "who's", "wouldn't", 'no', "you're", '-', 'down', 'a', "he'll", 'him', 'ought', "he's", '$', 'their', '||', 'on', 'as', "why's", '~', 'herself', 'than', 'his', "shan't", "she'll", 'hers', 'who', 'does', 'what', "when's", '<', '|', "haven't", 'yourselves', "you'd", '_', 'during', 'over', 'has', 'i', "where's", 'would', 'your', 'that', "didn't", '.', 'further', 'you', "you've", 'are', 'about', 'and', 'few', 'in', 'which', '"', '[', 'own', "they'd", 'its', 'while', 'or', 'ourselves', '@', "i've", 'most', "that's", 'below', 'do', '=', "can't", 'should', 'some', 'to', 'once', "aren't", ')', 'all', "she'd", 'more', 'we', 'where', ':', "wasn't", 'cannot', '\\', 'our', 'could', 'up', "we're", 'by', 'against', 'her', 'them', "we've", "couldn't", '#', 'any', "i'd", 'then', 'too', 'were', 'after', 'my', "weren't", 'until', 'whom', 'from', 'nor', "we'd", '`', 'itself', "i'm", 'so', "they've", "don't", "hasn't", 'same', '+', "i'll", 'have', '%', '?', 'is', 'myself', "doesn't", 'off', 'again', 'theirs', 'yourself', 'here', 'the', 'was', 'those', 'yours', 'such', 'at', "hadn't", "we'll", ']', 'only', 'being', "how's", 'me', 'out', '>', "mustn't", 'before', 'be', "they'll", 'with', '&', '(', 'how', 'there'}
	restrict = 1000
	new_query = []
	old_query = s.split()
	for word in old_query:
		if word not in stop_words:
			new_query.append(word)
	if len(new_query) == 0:
		return old_query
	else:
		return new_query


# indexindex = dict()
# alpha_path = os.path.dirname(os.getcwd()) + "/index/alphabet.json"
# with open(alpha_path) as alpha:
# 	indexindex = json.load(alpha)
# main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
# urlindex = get_url_index()
# urlrank = get_url_ranking()

# results = []
# seen = dict()
# words = dict()
# used = set()
# heap = []
# heapq.heapify(heap)
# front, end = (0, 1000)

# query = query_processing(query_processor(input()))

# start = time.time()
# for token in query:
# 	postings = find_postings(token, main_path, indexindex)[front:end]
# 	words[token] = postings

# 	for post in postings:
# 		if post["docID"] not in seen:
# 			seen[post["docID"]] = 1
# 		else:
# 			seen[post["docID"]] += 1
# 		score = sum_score(query, post["docID"], words, urlrank, urlindex, seen)
# 		heapq.heappush(heap, (-score, post["docID"]))


# for i in range(21):
# 	node = heapq.heappop(heap)
# 	if node and node[1] not in used:
# 		print(node)
# 		results.append(urlindex[str(node[1])])
# 		used.add(node[1])

# print(results)
# print(seen)

# end = time.time()


# print(end - start)


