from flask import Flask, render_template, escape, request, url_for, redirect
from search import Search
from textprocessing import query_processor
from test import sum_score, query_processing
from retrieval import get_index_index, get_url_index, get_threshold_index, get_url_ranking, find_postings, get_anchor
import heapq
import os

import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aab774a98e91dbc255f8ac641798d3de'


class Searcher:
	def __init__(self, q, ):
		self.old_query = q
		self.heap = []
		self.results = []
		self.words = dict() # key = token, value = list of postings, postings = dictionary
		self.seen = dict() # key = docID, value = number of times seen
		self.used = set() # ids
		self.threshold = 300
		self.front = 0
		self.end = self.threshold
		heapq.heapify(self.heap)

	def add_more(self, query, main_path, indexindex, urlrank, urlindex, anchor):
		# for each word, retrieve the postings, score each, and add to heap
		print(self.threshold)
		for token in query:
				postings = find_postings(token, main_path, indexindex)
				if postings:
					postings = postings[self.front:self.end]
				self.words[token] = postings

				if postings:
					for post in postings:
						if post["docID"] not in self.seen:
							self.seen[post["docID"]] = 1
						else:
							self.seen[post["docID"]] += 1
						score = sum_score(query, post["docID"], self.words, urlrank, urlindex, self.seen, anchor)
						heapq.heappush(self.heap, (-score, post["docID"]))
		self.front += self.threshold
		self.end += self.threshold
	
	def top(self, urlindex):
		self.results.append("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
		count = 0
		if len(self.heap) != 0:
			while len(self.heap) != 0 and count <= 20:
				node = heapq.heappop(self.heap)
				if node and node[1] not in self.used:
					self.results.append(urlindex[str(node[1])])
					self.used.add(node[1])
					count += 1
		else:
			self.results += ["No Results Found"]
		return self.results

	def change_threshold(self, threshold):
		print("fcu")
		self.threshold = threshold



indexindex = get_index_index()
urlindex = get_url_index()
threshold_index = get_threshold_index()
urlrank = get_url_ranking()
anchor = get_anchor()
main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
searcher = Searcher("")




@app.route('/', methods =['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	
	search = Search()
	time_passed = 0
	results = []
	print(main_path)
	global searcher

	if search.validate_on_submit():
		start = time.time()
		query, restrict = query_processing(query_processor(search.query.data), threshold_index)
		# DISPLAY MORE
		
		if search.query.data == searcher.old_query:
			searcher.add_more(query, main_path, indexindex, urlrank, urlindex, anchor)
			results = searcher.top(urlindex)

		# NEW QUERY
		else:
			searcher = Searcher(search.query.data)
			if restrict > 3:
				searcher.change_threshold(100)
			searcher.add_more(query, main_path, indexindex, urlrank, urlindex, anchor)
			results = searcher.top(urlindex)

		time_passed = time.time() - start
		time_passed = float(str(time_passed)[0:6])

	return render_template('home.html', title = 'Home', search = search, results = results, time_passed = time_passed)


if __name__ == '__main__':
	app.run(debug=True)