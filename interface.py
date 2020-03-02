from flask import Flask, render_template, escape, request, url_for, redirect
from search import Search
from main import get_results
from retrieval import get_index_index, get_url_index, get_threshold_index
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aab774a98e91dbc255f8ac641798d3de'

indexindex = get_index_index()
urlindex = get_url_index()
threshold_index = get_threshold_index()

@app.route('/', methods =['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    search = Search()
    results = []
    start = time.time()
    if search.validate_on_submit():
        results = get_results(search.query.data, indexindex, urlindex, threshold_index)[0:100]
    end = time.time()
    print("time elapsed =", end - start)
    return render_template('home.html', title = 'Home', search = search, results = results)

if __name__ == '__main__':
    app.run(debug=True)