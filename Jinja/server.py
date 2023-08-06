# Day 57 - Templating with Jinja
# Challenge 1 is also here - Gender and Age guessing website

from flask import Flask, render_template
import random
from datetime import datetime
import requests

app = Flask(__name__)
year = datetime.now().year

@app.route("/")
def home_page():
    # In order to show a random number, we'll need to use kwargs of render_template()
    return render_template("index.html", rand_num=random.randint(1, 10), year=year)


@app.route("/guess/<name>")
def guess(name):
    """Displays the guessed age and gender of a given name"""
    age_response = requests.get(f"https://api.agify.io?name={name}")
    gender_response = requests.get(f"https://api.genderize.io?name={name}")
    age = age_response.json()["age"]
    gender = gender_response.json()["gender"]
    return render_template("guess.html", name=name.capitalize(), age=age, gender=gender, year=year)


@app.route("/blog")
def blog():
    """Blog webpage (uses jinja multiline statements)"""
    blog_response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")  # Getting random blogs
    blogs = blog_response.json()
    return render_template("blog.html", blogs=blogs)


if __name__ == "__main__":
    app.run(debug=True)