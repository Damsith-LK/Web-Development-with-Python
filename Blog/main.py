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
    return render_template("post.html", title=title, body=body, subtitle=subtitle, date=date, id=id, year=year)

@app.route("/about")
def about():
    return render_template("about.html", year=year)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    # h1_message indicates what should be shown in the h1 of '/contact' page depending on method (get or post)
    # I think this would be a better approach than adding 'if's in html file with Jinja
    if request.method == "GET":
        return render_template("contact.html", h1_message="Contact Me", year=year)
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        print(name)
        print(email)
        print(phone)
        print(message)
        return render_template("contact.html", h1_message="Successfully sent your message", year=year)


if __name__ == "__main__":
    app.run(debug=True)
