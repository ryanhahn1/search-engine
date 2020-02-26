import json
import re
from bs4 import BeautifulSoup
import krovetz



#things we need:
# frequency of each word
# total number of terms
# important words vs normal
# 
def extract_text(json_data):
    try:
         if json_data:
            web_content = json_data["content"]
            soup = BeautifulSoup(web_content, "html.parser")
            count = 0

            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()

            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text

    except Exception as e:
        print(e)

# <strong> tags as important? Or only <bold>, <h1>, <h2>, <h3>, and <title>
def extract_important(json_data):
    try:
         if json_data:
            web_content = json_data["content"]
            soup = BeautifulSoup(web_content, "html.parser")
            count = 0
            text = ""

            for script in soup(["script", "style"]):
                script.decompose()

            for script in soup(["strong", "bold", "h1", "h2", "h3", "title"]):
                text += script.get_text() + " "
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text

    except Exception as e:
        print(e)

    
def tokenizer(token) -> dict:
    ks = krovetz.PyKrovetzStemmer()
    frequency = dict()
    for t in token:
        stemmed = ks.stem(t)
        count = frequency.get(stemmed, 0)
        frequency[stemmed] = count + 1
    return frequency #returns dictionary of terms: count

def query_processor(s):
    query = re.sub('[^a-z0-9]', ' ', s.lower()).split()
    new_query = ""
    ks = krovetz.PyKrovetzStemmer()
    for q in query:
        new_query += ks.stem(q) + " "
    return new_query

