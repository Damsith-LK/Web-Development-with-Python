# Day 56
# Here I'm going to make a personal website (a name card) using Flask (gonna use html, css too)
# A separate folder named 'templates' is where the html files should go
# And a folder named 'static' is where static files such as css and images should go
# Using a website template here
# Note: This is a learning project

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)