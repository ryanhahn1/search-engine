from flask import Flask, render_template, escape, request, url_for
# import main

app = Flask(__name__)

# results = getResults() a list of results

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

# results = getResults() a list of results
results = ["hello", "bye", "why"]
size = len(results)

@app.route('/results')
def output():
    return render_template('results.html', title = 'Results',results = results, size = size)

if __name__ == '__main__':
    app.run(debug=True)