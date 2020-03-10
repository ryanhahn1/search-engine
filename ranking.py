from retrieval import get_url_index
import networkx as nx
from bs4 import BeautifulSoup
from scanner import get_files
import re
import json
import os

def createGraph(Documents):
    directory = os.path.dirname(os.getcwd()) + "/index/"
    G = nx.DiGraph()
    url_links = get_url_index()
    url_link_dict = {y:x for x,y in url_links.items()}
    url_set = set(url_link_dict.keys())
    n = 0
    for doc in Documents:
        n += 1
        print(n)
        with open(doc, encoding='utf-8', errors='replace') as json_file:
            if ".DS_Store" not in doc:
                data = json.load(json_file)
                soup = BeautifulSoup(data['content'], 'html.parser')
                for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
                    if link.get('href') in url_set:
                        G.add_edge(n, int(url_link_dict.get(link.get('href'))))
                    else:
                        G.add_edge(n, link.get('href'))
    pr = nx.pagerank(G)

    file_name = os.path.join(directory, "url_ranking.json")
    with open(file_name, 'w') as url_file:
        json.dump(pr, url_file)
    print("ranking finished")

def anchorExtractor(Documents):
    directory = os.path.dirname(os.getcwd()) + "/index/"
    url_links = get_url_index()
    url_link_dict = {y:x for x,y in url_links.items()} #dict where keys are url's and values are ints
    url_set = set(url_link_dict.keys()) #set of relevant url's in corpus
    n = 0
    anchor_dict = dict()
    for doc in Documents:
        n+=1
        print(n)
        with open(doc, encoding='utf-8', errors='replace') as json_file:
            if ".DS_Store" not in doc:
                data = json.load(json_file)
                soup = BeautifulSoup(data['content'], 'html.parser')
                for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
                    link_url = link.get('href')
                    if link_url in url_set:
                        if len(link.text) > 3:
                            if anchor_dict.get(link_url, None) == None:
                                a = set()
                            else:
                                a = anchor_dict.get(link_url)
                            a.add(link.text)
                            anchor_dict[link_url] = a
    file_name = os.path.join(directory, "anchors.json")
    with open(file_name, 'w') as url_file:
        json.dump(anchor_dict, url_file)
    print("anchors found") 

# def update_pagerank(path):
# 	print("updating pagerank scores")
# 	new_path = os.path.dirname(os.getcwd()) + "/index/main.txt"
# 	scored = open(new_path, 'w')
# 	index = open(path, "r")
# 	for line in index:
# 		word, list_str = line.split(" ", 1)
# 		#print(word)
# 		list_real = json.loads(list_str)
# 		for post in list_real:
# 			post["score"] = score(post, 55393, len(list_real))
# 		list_real = sorted(list_real, key = lambda x: -x["score"])
# 		s = word + " " + json.dumps(list_real) + "\n"
# 		scored.write(s)
# 	index.close()
# 	scored.close()
# 	print("generated ranked")

if __name__ == "__main__":
    file_location = "DEV"
    # anchorExtractor(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location)))
    createGraph(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location)))
