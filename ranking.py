from retrieval import get_url_index
import networkx as nx
from bs4 import BeautifulSoup
from scanner import get_files
import re
import json
import os

def createGraph(Documents):
    directory = os.path.dirname(os.getcwd()) + "/index/"
    G = nx.Graph()
    url_link_dict = get_url_index()
    url_set = set(url_link_dict.values())
    n = 0
    for doc in Documents:
        n += 1
        print(n)
        with open(doc, encoding='utf-8', errors='replace') as json_file:
            if ".DS_Store" not in doc:
                data = json.load(json_file)
                soup = BeautifulSoup(data['content'], 'html.parser')
                for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                    if link.get('href') in url_set:
                        G.add_edge(n, url_link_dict.get(link.get('href')))
    H = nx.DiGraph(G)
    pr = nx.pagerank(H, alpha=0.9)
    file_name = os.path.join(directory, "url_ranking.json")
    with open(file_name, 'w') as url_file:
        json.dump(pr, url_file)
    print("ranking finished")


if __name__ == "__main__":
    file_location = "DEV"
    createGraph(get_files(os.path.join(os.path.dirname(os.getcwd()), file_location)))
