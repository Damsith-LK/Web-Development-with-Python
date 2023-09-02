# Day 66 - Learning about RESTful APIs and building my own REST API
"""
There are two requirements for an API to be RESTful:
    1. Use HTTP verbs eg-GET
    2. Use specific patterns of routes/endpoint URLs
"""
"""
Challenge 1 - create a /random route that serves up a random cafe.
"""

from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import random as rand_lib

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def random():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    rand_cafe = rand_lib.choice(cafes)
    # Serialization - Turning into JSON
    return jsonify(
        cafe={
            "id": rand_cafe.id,
            "name": rand_cafe.name,
            "map_url": rand_cafe.map_url,
            "img_url": rand_cafe.img_url,
            "location": rand_cafe.location,
            "seats": rand_cafe.seats,
            "has_toilet": rand_cafe.has_toilet,
            "has_wifi": rand_cafe.has_wifi,
            "has_sockets": rand_cafe.has_sockets,
            "can_take_calls": rand_cafe.can_take_calls,
            "coffee_price": rand_cafe.coffee_price
        }
    )


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
