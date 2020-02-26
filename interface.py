from flask import Flask, render_template, escape, request, url_for, redirect
from search import Search
import main

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aab774a98e91dbc255f8ac641798d3de'

results = []

@app.route('/', methods =['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    search = Search()
    if search.validate_on_submit():
        results.append(search.query.data)
        return redirect(url_for('output'))
    return render_template('home.html', title = 'Home', search = search)

@app.route('/results')
def output():
    return render_template('results.html', title = 'Results',results = results, size = size)

if __name__ == '__main__':
    app.run(debug=True)