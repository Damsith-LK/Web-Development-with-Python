# Day 63 - Building a virtual library and also learn about some SQL things
# This is a super simple project made to practise CRUD with SQLAlchemy
"""
Features of this Virtual Library:
    1. Show books that are already in the library (Read)
    2. Add more books to the library (Create)
    3. Edit the rating of each book in the library (Update)
    4. Delete books and their related stuff from library (Delete)
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///virtual-library.db"
db.init_app(app)

# Create table
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

# Schema
with app.app_context():
    db.create_all()


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        author = request.form["author"]
        rating = request.form["rating"]
        print(name, author, rating)
        # Create a new record to DB
        with app.app_context():
            new_book = Books(title=name, author=author, rating=rating)
            db.session.add(new_book)
            db.session.commit()
    # Read from DB
    with app.app_context():
        all_books = db.session.execute(db.select(Books).order_by(Books.title)).scalars().all()

    return render_template("index.html", books=all_books)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        book_id = request.args.get("id")
        # Read from DB
        with app.app_context():
            to_update_book = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
        return render_template("edit.html", book=to_update_book)
    else:
        update_book_rating = request.form["new_rating"]
        book_id = request.form["id"]  # Hidden <input> in edit.html
        with app.app_context():
            to_update_book = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
            to_update_book.rating = update_book_rating
            db.session.commit()
            return redirect(url_for("home"))


@app.route("/delete", methods=["POST", "GET"])
def delete():
    book_id = request.args.get("id")
    if book_id is not None:
        with app.app_context():
            del_book = db.get_or_404(Books, book_id)
            db.session.delete(del_book)
            db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)