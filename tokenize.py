import json
import re
from bs4 import BeautifulSoup


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

def tokenize(s):
    token = set(re.sub('[^a-z0-9]', ' ', s.lower()).split())
    

    return token


path = "C:/Users/raynh/Desktop/assignment3/analyst/www_informatics_uci_edu/0a3175bebaa8bab4bc69961115bf3cebf8c6337ae6a62394c8e5e2d5509ddcee.json"

with open(path) as json_file:
    data = json.load(json_file)
    #print(data["encoding"])
    output = extract_text(data)
    tokens = tokenize(output)
    print(tokens)