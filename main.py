from retrieval import find_all_boolean, get_index_index, find_postings, get_url_index, get_threshold_index, get_url_ranking
from textprocessing import query_processor

import os
import json 
import time

def get_results(input, index_index, url_index, threshold_index, urlrank):
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	query = query_processor(input)
	ranking = []
	results = find_all_boolean(query, main_path, index_index, threshold_index, urlrank, url_index)
	if results:
		count = 0
		for docid, value in sorted(results.items(), key=lambda x: -x[1]):
			#if count < 11:
				#print(url_index[str(docid)], value)
			ranking.append(url_index[str(docid)])
			#count += 1
		return ranking
	else:
		return ["No Matching Results"]


if __name__ == '__main__':
	
	
	indexindex = get_index_index()
	urlindex = get_url_index()
	threshold_index = get_threshold_index()
	urlrank = get_url_ranking()
	query = input()
	start = time.time()
	get_results(query, indexindex, urlindex, threshold_index, urlrank)
	end = time.time()
	print("time", end-start)
