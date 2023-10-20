# Day 68 - Authentication with Flask

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)


# CREATE TABLE IN DB
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
 
 
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """Register new users to website"""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"].lower()
        password = request.form["password"]
        # Check if inputted email already exist in DB. If so, redirect user to login page
        check_email = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if check_email:
            flash("You have already signed up with that email. Log in instead.")
            return redirect(url_for("login"))
        # Hashing and salting the password. This makes it super secure
        password = generate_password_hash(password=password, method="pbkdf2:sha256", salt_length=8)
        # Creating a new entry in DB
        new_user = User(
            email=email,
            password=password,
            name=name
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("secrets", name=name))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the users. Uses Flask flash"""
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]
        # Check whether the given email exist in the DB or not
        check_email = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not check_email:
            flash("This email does not exist. Please try again.", "error")
        else:
            # Check if the given password is correct. (Compare password hash and the inputted password)
            check_password = check_password_hash(check_email.password, password)
            if not check_password:
                flash("Password incorrect. Please try again.", "error")

    return render_template("login.html")


@app.route('/secrets')
def secrets():
    name = request.args.get("name")
    return render_template("secrets.html", name=name)


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    """Download the cheat sheet to user's device"""
    return send_from_directory(
        directory="static/files",
        path="cheat_sheet.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
