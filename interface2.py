from flask import Flask, render_template, escape, request, url_for, redirect
from search import Search
from textprocessing import query_processor
from test import sum_score
from retrieval import get_index_index, get_url_index, get_threshold_index, get_url_ranking, find_postings
import heapq

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
    
    if search.validate_on_submit():
    	start = time.time()
    	used = set()
    	heap = []
    	heapq.heapify(heap)
    	front, end = (0, 300)
        query = query_processor(search.query.data)

        for token in query:
        	postings = find_postings(token, main_path, indexindex)[front:end]
        	words[token] = postings

        	for post in postings:
        		if post["docID"] not in seen:
					seen[post["docID"]] = 1
				else:
					seen[post["docID"]] += 1
				score = sum_score(query, post["docID"], words, urlrank, urlindex, seen)
				heapq.heappush(heap, (-score, post["docID"]))
		for i in range(20):
			node = heapq.heappop(heap)
			if node and node[1] not in used:
				results.append(url_index[str(node[1])])
				used.add(node[1])
				
    end = time.time()
    print("time elapsed =", end - start)
    return render_template('home.html', title = 'Home', search = search, results = results)




if __name__ == '__main__':
    app.run(debug=True)