from flask import Flask, render_template, escape, request, url_for, redirect
from search import Search
from textprocessing import query_processor
from test import sum_score, query_processing
from retrieval import get_index_index, get_url_index, get_threshold_index, get_url_ranking, find_postings
import heapq
import os

import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aab774a98e91dbc255f8ac641798d3de'

indexindex = get_index_index()
urlindex = get_url_index()
threshold_index = get_threshold_index()
urlrank = get_url_ranking()
main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"

@app.route('/', methods =['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	search = Search()
	results = []
	time_passed = 0
	if search.validate_on_submit():
		start = time.time()
		used = set()
		heap = []
		words = dict()
		seen = dict()
		heapq.heapify(heap)
		front, end = (0, 1000)
		query = query_processing(query_processor(search.query.data))

		for token in query:
			postings = find_postings(token, main_path, indexindex)
			if postings:
				postings = postings[front:end]
			words[token] = postings


			if postings:
				for post in postings:
					if post["docID"] not in seen:
						seen[post["docID"]] = 1
					else:
						seen[post["docID"]] += 1
					score = sum_score(query, post["docID"], words, urlrank, urlindex, seen)
					heapq.heappush(heap, (-score, post["docID"]))

		count = 0
		if len(heap) != 0:
			while len(heap) != 0 and count <= 20:
				node = heapq.heappop(heap)
				if node and node[1] not in used:
					results.append(urlindex[str(node[1])])
					used.add(node[1])
				count += 1
		else:
			results = ["No Results Found"]
		time_passed = time.time() - start
		
	return render_template('home.html', title = 'Home', search = search, results = results, time_passed = time_passed)




if __name__ == '__main__':
    app.run(debug=True)