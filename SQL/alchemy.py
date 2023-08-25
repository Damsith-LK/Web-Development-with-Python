# Day 63 - Alchemy
# There's a much better way to deal with SQL instead of writing everything manually like in sqlite.py file
# Install flask-sqlalchemy with pip install -U Flask-SQLAlchemy

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

with app.app_context():
    new_book = Books(id=2, title="Harry Potter 2", author="J.K.Rowling", rating=8)
    db.session.add(new_book)
    db.session.commit()