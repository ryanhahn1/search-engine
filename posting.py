import math

# helper function to create a posting dictionary
def create_posting(docid, frequency, important, wordcount):
    post = dict()
    post["docID"] = docid
    post["word_count"] = wordcount
    post["term_freq"] = frequency
    post["importance"] = important
    post["score"] = 0
    return post