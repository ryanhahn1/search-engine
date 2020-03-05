from retrieval import find_all_boolean, get_index_index
from textprocessing import query_processor

import os
import json 

def get_results(input, index_index, url_index, threshold_index):
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	query = query_processor(input)
	ranking = []
	results = find_all_boolean(query, main_path, index_index, threshold_index)
	if results:
		for docid, value in sorted(results.items(), key=lambda x: -x[1]):
			ranking.append(url_index[str(docid)])
		return ranking
	else:
		return ["No Matching Results"]

"""if __name__ == '__main__':
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	url_index_file = os.path.dirname(os.getcwd()) + "/index/url_index.json"
	indexindex = get_index_index()
	with open(url_index_file) as json_file:
		url_index = json.load(json_file)

	query = query_processor(input())
	results = find_all_boolean(query, main_path, indexindex)
	ranking = []

	if results:
		for docid, value in sorted(results.items(), key=lambda x: -x[1]):
			# print(docid)
			ranking.append(url_index[str(docid)])

	else:
		print("fuck you")"""