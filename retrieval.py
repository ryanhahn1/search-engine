import os
import json
import math
from textprocessing import query_processor

def get_anchor():
	anchor_path = os.path.dirname(os.getcwd()) + "/index/anchor.json"
	with open(anchor_path) as anchor:
		result = json.load(anchor)
	return result

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

def get_url_ranking():
	url_rank_file = os.path.dirname(os.getcwd()) + "/index/url_ranking.json"
	with open(url_rank_file) as json_file:
		url_rank = json.load(json_file)
	return url_rank

# returns the list of postings for a query term
def find_postings(token, index_path, indexindex):
	if token in indexindex:
		next_pos = indexindex[token]
		with open(index_path, "r") as index:
			index.seek(next_pos)
			line = index.readline()
			word = line.split(" ", 1)[0]
			list_str = line.split(" ", 1)[1]
			if word == token:
				return json.loads(list_str)
	return None

# computes the document score for a query, including pagerank, anchor text, etc
def sum_score(query, id, words, urlrank, urlindex, seen, anchor):
	importance_sum = 1
	url_sum = 1
	score_sum = 0
	token_length = 0
	score_length = 0
	boolean_sum = 1
	page_score = 1
	anchor_score = 1

	#set page rank score
	if str(id) in urlrank:
		page_score = (1 + urlrank[str(id)] * 10000)
	
	for token in query:
		if token in words:
			p = [p for p in words[token] if p["docID"] == id]
			if len(p) >= 1:
				#IMPORTANT
				if p[0]["importance"]:
					importance_sum = importance_sum * 3
				#ANCHOR TEXT
				if str(id) in anchor and token in anchor[str(id)]:
					#print("ANCHOR", token, urlindex[str(id)].lower())
					anchor_score = 1.5
				#URL
				if token in urlindex[str(id)].lower():
					url_sum = url_sum * 1.1
				if seen[id] == len(query):
					boolean_sum = 100
				# COSINE
				doc_score = p[0]["score"]
				token_score = query.count(token) * (55393 / len(words[token]))
				# add the vectors to the sums
				token_length += token_score ** 2
				score_length += doc_score ** 2
				score_sum += doc_score * token_score
	return anchor_score * page_score * url_sum * importance_sum * boolean_sum * (score_sum / math.sqrt(token_length * score_length))

# returns a tuple of the query to use in retrieval and the restriction level
def query_processing(s, threshold):
	stop_words = {'been', 'ours', "they're", 'when', 'into', '}', 'each', 'having', 'very', 'himself', 'between', 'they', 'this', "won't", '{', 'it', ',', "here's", 'not', "she's", 'am', "let's", 'other', 'under', "he'd", 'both', '^', 'if', 'he', 'themselves', '*', 'an', 'why', '!', "what's", 'but', 'doing', 'because', ';', 'of', "you'll", "there's", "it's", 'these', '/', 'for', "shouldn't", 'above', 'did', 'had', "isn't", 'she', 'through', "who's", "wouldn't", 'no', "you're", '-', 'down', 'a', "he'll", 'him', 'ought', "he's", '$', 'their', '||', 'on', 'as', "why's", '~', 'herself', 'than', 'his', "shan't", "she'll", 'hers', 'who', 'does', 'what', "when's", '<', '|', "haven't", 'yourselves', "you'd", '_', 'during', 'over', 'has', 'i', "where's", 'would', 'your', 'that', "didn't", '.', 'further', 'you', "you've", 'are', 'about', 'and', 'few', 'in', 'which', '"', '[', 'own', "they'd", 'its', 'while', 'or', 'ourselves', '@', "i've", 'most', "that's", 'below', 'do', '=', "can't", 'should', 'some', 'to', 'once', "aren't", ')', 'all', "she'd", 'more', 'we', 'where', ':', "wasn't", 'cannot', '\\', 'our', 'could', 'up', "we're", 'by', 'against', 'her', 'them', "we've", "couldn't", '#', 'any', "i'd", 'then', 'too', 'were', 'after', 'my', "weren't", 'until', 'whom', 'from', 'nor', "we'd", '`', 'itself', "i'm", 'so', "they've", "don't", "hasn't", 'same', '+', "i'll", 'have', '%', '?', 'is', 'myself', "doesn't", 'off', 'again', 'theirs', 'yourself', 'here', 'the', 'was', 'those', 'yours', 'such', 'at', "hadn't", "we'll", ']', 'only', 'being', "how's", 'me', 'out', '>', "mustn't", 'before', 'be', "they'll", 'with', '&', '(', 'how', 'there'}
	restrict = 1000
	new_query = []
	old_query = s.split()
	for word in old_query:
		if word not in stop_words:
			if word in threshold:
				restrict = min(restrict, math.floor(math.log10(threshold[word])))
			new_query.append(word)
	if len(new_query) == 0:
		return (old_query, restrict)
	else:
		return (new_query, restrict)