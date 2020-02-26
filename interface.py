from flask import Flask, render_template, escape, request, url_for, redirect
from search import Search
from main import get_results
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aab774a98e91dbc255f8ac641798d3de'

@app.route('/', methods =['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    search = Search()
    results = []
    start = time.time()
    if search.validate_on_submit():
        results = get_results(search.query.data)
    end = time.time()
    print("time elapsed =", end - start)
    return render_template('home.html', title = 'Home', search = search, results = results)

if __name__ == '__main__':
    app.run(debug=True)