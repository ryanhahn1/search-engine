def scan_documents():
    simhashes = set() #simhash object
    tokens = dict() #key = word, value = number of instances
    pagecount = 0
    longest = ['', 0]