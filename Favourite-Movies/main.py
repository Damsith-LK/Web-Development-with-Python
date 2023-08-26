# Day 64 - My Top 10 Favourite Movies Website
"""
Requirements of this website
    1. Be Able to View Movie List Items - Done
    2. Be Able to Edit a Movie's Rating and Review - Done
    3. Be Able to Delete Movies from the Database - Done
    4. Be Able to Add New Movies Via the Add Page - Done
    5. Be Able to Sort and Rank the Movies By Rating
"""
# Don't confuse 'requests' for API get and 'request' in flask

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
import config
import requests

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies-database.db"
db.init_app(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
# Headers for TMDB requesting
tmdb_headers = {"accept": "application/json", "Authorization": config.tmdb_key}

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

# Form to add new movies into the database
class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


def get_movies(title) -> list:
    """This function is for getting the relevant information about movies according to the given input from TMDB API.
    Use this inside add() function"""
    api_url = "https://api.themoviedb.org/3/search/movie"
    params = {"query": title}
    response = requests.get(api_url, params=params, headers=tmdb_headers).json()
    return response["results"]

def get_movie_info(movie_id) -> list:
    """Gets the information about the movie corresponding to the given id.
    The list outputs = [title, img_url, year, description]"""
    api_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(api_url, headers=tmdb_headers).json()
    title = response["title"]
    img_url = f"https://image.tmdb.org/t/p/w500{response['poster_path']}"
    year = response["release_date"].split("-")[0]
    description = response["overview"]
    return [title, img_url, year, description]


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


@app.route("/delete", methods=["POST", "GET"])
def delete():
    movie_id = request.args["id"]
    if movie_id is not None:
        to_del_movie = db.get_or_404(Movie, movie_id)
        db.session.delete(to_del_movie)
        db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["POST", "GET"])
def add():
    """For adding new movies into the database"""
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        movie_title = add_form.title.data
        movies_info = get_movies(movie_title)
        return render_template("select.html", movies=movies_info)
        # return redirect(url_for('home'))
    return render_template("add.html", form=add_form)


@app.route("/select", methods=["POST", "GET"])
def select():
    """This func gets the information of the movie, user selected in /add and creates a new entry in DB. The information is requested form TMDB"""
    movie_id = request.args["id"]
    title, img_url, year, description = get_movie_info(movie_id)
    # Instance of Movie
    new_movie = Movie(title=title, year=year, description=description, img_url=img_url, rating=0, review="Null", ranking=0)
    # Creating a new entry in DB
    with app.app_context():
        db.session.add(new_movie)
        db.session.commit()
        # Reading the id of the movie for /edit
        movie_id_in_db = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar().id
    # Redirecting to /edit page in order to add a rating and a review to the movie
    return redirect(url_for('edit', id=movie_id_in_db))

if __name__ == '__main__':
    app.run(debug=True)
