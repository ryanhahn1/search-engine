import math

# class Posting():
#     def __init__(self, id, frequency, important, wordcount):
#         self.docID = id
#         # self.postings
#         self.word_count = wordcount
#         self.term_freq = frequency
#         self.idf = 0
#         self.importance = important
    
#     # calculates and sets the idf attribute
#     def set_idf(self, total_docs, total_with_term):
#         self.idf = log( (total_docs / total_with_term) )

#     # calculates and returns the tf-idf
#     def get_tfidf(self):
#         return ( (term_freq / word_count) / self.idf )

def create_posting(docid, frequency, important, wordcount):
    post = dict()
    post["docID"] = docid
    post["word_count"] = wordcount
    post["term_freq"] = frequency
    post["idf"] = 0
    post["importance"] = important
    return post

# total_with_term = length of postings list for that word
def set_idf(self, post, total_docs, total_with_term):
    post["idf"] = log( (total_docs / total_with_term) )

# calculates and returns the tf-idf
def get_tfidf(self, post):
    return ( (post["term_freq"] / post["word_count"]) / post["idf"] )