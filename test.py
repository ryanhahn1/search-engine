import time 
import json
import os
import heapq
import math
from retrieval import find_postings, get_url_index, get_url_ranking, get_threshold_index, get_anchor
from textprocessing import query_processor


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
	print(restrict)
	if len(new_query) == 0:
		return (old_query, restrict)
	else:
		return (new_query, restrict)

if __name__ == '__main__':
	indexindex = dict()
	alpha_path = os.path.dirname(os.getcwd()) + "/index/alphabet.json"
	with open(alpha_path) as alpha:
		indexindex = json.load(alpha)
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	urlindex = get_url_index()
	urlrank = get_url_ranking()
	threshold_index = get_threshold_index()
	anchor_index = get_anchor()

	results = []
	seen = dict()
	words = dict()
	used = set()
	heap = []
	heapq.heapify(heap)
	front, end = (0, 1000)

	query, restrict = query_processing(query_processor(input()), threshold_index)

	start = time.time()
	for token in query:
		postings = find_postings(token, main_path, indexindex)[front:end]
		words[token] = postings

		for post in postings:
			if post["docID"] not in seen:
				seen[post["docID"]] = 1
			else:
				seen[post["docID"]] += 1
			score = sum_score(query, post["docID"], words, urlrank, urlindex, seen, anchor_index)
			heapq.heappush(heap, (-score, post["docID"]))
			if post["docID"] == 53563:
				print(score)


	for i in range(21):
		node = heapq.heappop(heap)
		if node and node[1] not in used:
			print(node)
			results.append(urlindex[str(node[1])])
			used.add(node[1])

	print(results)

	end = time.time()


	print(end - start)


