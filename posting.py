import math

class Posting():
    def __init__(self, id, frequency, important, wordcount):
        self.docID = id
        # self.postings
        self.word_count = wordcount
        self.term_freq = frequency
        self.idf = 0
        self.importance = important
    
    # calculates and sets the idf attribute
    def set_idf(self, total_docs, total_with_term):
        self.idf = log( (total_docs / total_with_term) )

    # calculates and returns the tf-idf
    def get_tfidf(self):
        return ( (term_freq / word_count) / self.idf )