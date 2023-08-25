# Day 63 - SQLAlchemy
# There's a much better way to deal with SQL instead of writing everything manually like in sqlite.py file
# Install flask-sqlalchemy with pip install -U Flask-SQLAlchemy
# CRUD operations = Create, Read, Update, Delete

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Going to do everything I did in sqlite this time using pip flask-sqlalchemy

# Initializations
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
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

# Creating a new record
# with app.app_context():
#     new_book = Books(id=2, title="Harry Potter 2", author="J.K.Rowling", rating=8)
#     db.session.add(new_book)
#     db.session.commit()

# Read all records
with app.app_context():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalar()

# Read A Particular Record By Query
with app.app_context():
    book = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()

# Update A Particular Record By Query
with app.app_context():
    to_update_book = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()
    to_update_book.title = "Harry Potter and the Prisoner of the Azkaban"
    db.session.commit()

# Update a particular query by PRIMARY KEY
with app.app_context():
    to_update_book_2 = db.session.execute(db.select(Books).where(Books.id == 2)).scalar()
    # or to_update_book_2 = db.get_or_404(Books, 2)
    to_update_book_2.title = "Harry Potter and the Chamber of Secrets"
    db.session.commit()

# Delete A Particular Record By PRIMARY KEY
with app.app_context():
    delete_book = db.session.execute(db.select(Books).where(Books.id == 2)).scalar()
    # or delete_book = db.get_or_404(Books, 2)
    db.session.delete(delete_book)
    db.session.commit()