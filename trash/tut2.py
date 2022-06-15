from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html')


@app.route("/about")
def about():
    name = "Archit"
    return render_template('about.html', name=name)


@app.route("/bootstrap")
def bootstrap():
    return render_template('bootstrap.html')

app.run(debug=True)
