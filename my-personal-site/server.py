# Day 56
# Here I'm going to make a personal website using Flask (gonna use html, css too)
# A separate folder named 'templates' is where the html, css files should go
# Note: This is a learning project

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)