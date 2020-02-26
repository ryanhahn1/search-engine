from retrieval import find_all_boolean

import os
import json 


if __name__ == '__main__':
	main_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
	url_index_file = os.path.dirname(os.getcwd()) + "/index/url_index.json"
	with open(url_index_file) as json_file:
		url_index = json.load(json_file)
	query = input()
	ranking = []


	for docid, value in sorted(find_all_boolean(query, main_path).items(), key=lambda x: -x[1]):
		# print(docid)
		ranking.append(url_index[str(docid)])

	count = 1
	while count < 11:
		print(count, ranking[count - 1])
		count += 1