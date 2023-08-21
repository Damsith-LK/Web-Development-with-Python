# Day 61 - Learning about WTForms
# There is a lib called Bootstrap-Flask which makes coding these even easier

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NoneOf
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = "wakeuptoreality"

class LoginForm(FlaskForm):
    """Creating a WTF class with inheritance"""
    email = StringField(label='Email', validators=[DataRequired(), Email(), NoneOf(values=".")])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Submit")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data.lower() == "admin@email.com" and login_form.password.data == "12345678":
            return render_template("success.html")
        return render_template("denied.html")
    return render_template("login.html", form=login_form)

if __name__ == '__main__':
    app.run(debug=True)
