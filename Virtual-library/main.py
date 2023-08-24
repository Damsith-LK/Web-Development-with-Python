# Day 63 - Building a virtual library and also learn about some SQL things

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        author = request.form["author"]
        rating = request.form["rating"]
        dictionary = {"title": name, "author": author, "rating": rating}
        all_books.append(dictionary)
        print(all_books)
    return render_template("index.html", books=all_books, book_len=len(all_books))


@app.route("/add")
def add():
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)