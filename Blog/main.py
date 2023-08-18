# Day 57 - Blog Capstone project
# Day 59 - Upgrading Blog

from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

response = requests.get("https://api.npoint.io/079a621441e20cdc107d")
content = response.json()
year = datetime.now().year

@app.route('/')
def home():
    return render_template("index.html", blogs=content, year=year)

# @app.route("/post/<int:num>")
# def post(num):
#     title = blogs[num-1]["title"]
#     body = blogs[num-1]["body"]
#     subtitle = blogs[num-1]["subtitle"]
#     return render_template("post.html", title=title, body=body, subtitle=subtitle)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
