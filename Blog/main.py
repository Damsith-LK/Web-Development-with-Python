# Day 57 - Blog Capstone project
# Day 59 - Upgrading Blog
# Day 60 - Getting the HTML forms to work

from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

response = requests.get("https://api.npoint.io/079a621441e20cdc107d")
blogs = response.json()
year = datetime.now().year

@app.route('/')
def home():
    return render_template("index.html", blogs=blogs, year=year)

@app.route("/post/<int:num>")
def post(num):
    title = blogs[num-1]["title"]
    body = blogs[num-1]["body"]
    subtitle = blogs[num-1]["subtitle"]
    date = blogs[num-1]["date"]
    id = blogs[num-1]["id"]
    return render_template("post.html", title=title, body=body, subtitle=subtitle, date=date, id=id)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        print(name)
        print(email)
        print(phone)
        print(message)
        return "<h1>Successfully sent your message</h1>"

# @app.route("/form-entry", methods=["POST"])
# def form_entry():
#     name = request.form["name"]
#     email = request.form["email"]
#     phone = request.form["phone"]
#     message = request.form["message"]
#     print(name)
#     print(email)
#     print(phone)
#     print(message)
#     return "<h1>Successfully sent your message</h1>"


if __name__ == "__main__":
    app.run(debug=True)
