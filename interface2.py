from flask import Flask, render_template, escape, request, url_for, redirect
from search import Search
from textprocessing import query_processor
from retrieval import sum_score, query_processing, get_index_index, get_url_index, get_threshold_index, get_url_ranking, find_postings, get_anchor
import heapq
import os

import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aab774a98e91dbc255f8ac641798d3de'

# class used to store retrieval state for search engine operation
class Searcher:
	def __init__(self, q, ):
		self.old_query = q
		self.heap = []
		self.results = []
		self.words = dict() # key = token, value = list of postings, postings = dictionary
		self.seen = dict() # key = docID, value = number of times seen
		self.used = set() # ids
		self.front = 0 # where to start adding postings
		self.end = 299 # where to end adding postings
		self.threshold = 300 # number of postings to add
		self.page_count = 1 # which batch is going to be displayed
		heapq.heapify(self.heap)

	# add the next batch of documents to the heap
	def add_more(self, query, main_path, indexindex, urlrank, urlindex, anchor):
		# for each word, retrieve the postings, score each, and add to heap
		for token in query:
				# retrieve postings
				postings = find_postings(token, main_path, indexindex)
				if postings:
					postings = postings[self.front:self.end]
				self.words[token] = postings
				# score postings and add to heap
				if postings:
					for post in postings:
						if post["docID"] not in self.seen:
							self.seen[post["docID"]] = 1
						else:
							self.seen[post["docID"]] += 1
						score = sum_score(query, post["docID"], self.words, urlrank, urlindex, self.seen, anchor)
						heapq.heappush(self.heap, (-score, post["docID"]))
		# increment the bounds for the next retrieval request
		self.front += self.threshold
		self.end += self.threshold
	
	# return the top set of documents from the heap
	def top(self, urlindex):
		self.results.append("///////////////////////////////////////////////////////////////////////////////" + " Page " + str(self.page_count) + " ///////////////////////////////////////////////////////////////////////////////")
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

	# change the number of documents to 
	def change_threshold(self, threshold):
		self.end = threshold - 1
		self.threshold = threshold


# load necessary files into memory
indexindex = get_index_index()
urlindex = get_url_index()
threshold_index = get_threshold_index()
urlrank = get_url_ranking()
anchor = get_anchor()
main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
searcher = Searcher("")
cache = dict() # key = query, value = heap




@app.route('/', methods =['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	search = Search()
	time_passed = 0
	results = []
	global searcher


	if search.validate_on_submit():
		start, end = 0, 0
		query, restrict = query_processing(query_processor(search.query.data), threshold_index)
		print(query)
		# DISPLAY MORE
		if search.query.data == searcher.old_query:
			start = time.time()
			searcher.add_more(query, main_path, indexindex, urlrank, urlindex, anchor)
			end = time.time()
			searcher.page_count += 1
			results = searcher.top(urlindex)
		# NEW QUERY
		else:
			searcher = Searcher(search.query.data)
			if restrict > 3:
				searcher.change_threshold(100)
				print(searcher.threshold)
			start = time.time()
			searcher.add_more(query, main_path, indexindex, urlrank, urlindex, anchor)
			end = time.time()
			results = searcher.top(urlindex)

		time_passed = end - start
		time_passed = float(str(time_passed)[0:6])

	return render_template('home.html', title = 'Home', search = search, results = results, time_passed = time_passed)


if __name__ == '__main__':
	app.run(debug=True)