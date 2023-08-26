# Day 64 - My Top 10 Favourite Movies Website
"""
Requirements of this website
    1. Be Able to View Movie List Items - Done
    2. Be Able to Edit a Movie's Rating and Review - Done
    3. Be Able to Delete Movies from the Database
    4. Be Able to Add New Movies Via the Add Page
    5. Be Able to Sort and Rank the Movies By Rating
"""

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
import requests

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies-database.db"
db.init_app(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# Create table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)

# Schema
with app.app_context():
    db.create_all()

# Form to edit rating and review of a movie
class RateMovieForm(FlaskForm):
    rating = FloatField(label="Your rating out of 10, eg.7.5", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField(label="Your Review", validators=[DataRequired(), Length(max=40)])
    submit = SubmitField(label="Done")


@app.route("/")
def home():
    with app.app_context():
        all_movies = db.session.execute(db.select(Movie).order_by(Movie.title)).scalars().all()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["POST", "GET"])
def edit():
    """For updating movie rating and review"""
    movie_id = request.args["id"]
    # Adding an if here to prevent unnecessary requests, eg: just /edit instead of /edit?id=some_id
    if movie_id is not None:
        edit_form = RateMovieForm()
        if edit_form.validate_on_submit():
            with app.app_context():
                to_update_movie = db.session.execute(db.Select(Movie).where(Movie.id == movie_id)).scalar()
                to_update_movie.rating = edit_form.rating.data
                to_update_movie.review = edit_form.review.data
                db.session.commit()
            return redirect(url_for('home'))
        return render_template("edit.html", form=edit_form)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)