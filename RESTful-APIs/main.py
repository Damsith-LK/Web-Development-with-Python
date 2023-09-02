# Day 66 - Learning about RESTful APIs and building my own REST API
"""
There are two requirements for an API to be RESTful:
    1. Use HTTP verbs eg-GET
    2. Use specific patterns of routes/endpoint URLs
"""
"""
Challenge 1 - create a /random route that serves up a random cafe. - Done
Challenge 2 - create a /all route that serves up all the cafes. - Done
Challenge 3 - create a /search route to search for cafes at a particular location. - Done
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


def format_json(id, name, map_url, img_url, loc, seats, has_toilet, has_wifi, has_sockets, can_take_calls, coffee_price):
    """Format jsons"""
    formatted_dict = {
        "id": id,
        "name": name,
        "map_url": map_url,
        "img_url": img_url,
        "location": loc,
        "seats": seats,
        "has_toilet": has_toilet,
        "has_wifi": has_wifi,
        "has_sockets": has_sockets,
        "can_take_calls": can_take_calls,
        "coffee_price": coffee_price
    }
    return formatted_dict


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def random():
    """"Fetches a random cafe"""
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    rand_cafe = rand_lib.choice(cafes)
    # Serialization - Turning into JSON
    return jsonify(
        cafe=format_json(rand_cafe.id, rand_cafe.name, rand_cafe.map_url, rand_cafe.img_url, rand_cafe.location, rand_cafe.seats,
                         rand_cafe.has_toilet, rand_cafe.has_wifi, rand_cafe.has_sockets, rand_cafe.can_take_calls, rand_cafe.coffee_price)
    )

@app.route("/all")
def all():
    """All the cafes in the DB"""
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    # Creating a list of dictionaries containing details about each cafe
    all_cafes = []
    # Iterating over each row in DB
    for cafe in cafes:
        cafe_dict = format_json(cafe.id, cafe.name, cafe.map_url, cafe.img_url, cafe.location, cafe.seats, cafe.has_toilet, cafe.has_wifi, cafe.has_sockets, cafe.can_take_calls, cafe.coffee_price)
        all_cafes.append(cafe_dict)
    return jsonify(cafes=all_cafes)


@app.route("/search")
def search():
    """Search cafes by location"""
    loc = request.args["loc"]
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location == loc.title())).scalars().all()
    # If there are cafes in the given location
    if len(cafes) > 0:
        search_cafes = []
        for cafe in cafes:
            cafe_dict = format_json(cafe.id, cafe.name, cafe.map_url, cafe.img_url, cafe.location, cafe.seats, cafe.has_toilet, cafe.has_wifi, cafe.has_sockets, cafe.can_take_calls, cafe.coffee_price)
            search_cafes.append(cafe_dict)
        return jsonify(search=search_cafes)
    else:
        return jsonify(
            error={
                "Not Found": "Sorry, we don't have a cafe at that location."
            }
        )


if __name__ == '__main__':
    app.run(debug=True)
