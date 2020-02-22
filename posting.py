import math

class Posting(self):
    def __init__(self, id, frequency, important, wordcount)
        self.docID = id
        # self.postings
        self.word_count = wordcout
        self.term_freq = frequency
        self.idf = 0
        self.importance = important
    
    # calculates and sets the idf attribute
    def set_idf(total_docs, total_with_term):
        self.idf = log( (total_docs / total_with_term) )

    # calculates and returns the tf-idf
    def get_tfidf():
        return ( (term_freq / word_count) / self.idf )