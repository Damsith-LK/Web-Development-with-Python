# Day 61 - Learning about WTForms

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
app.secret_key = "wakeuptoreality"

class MyForm(FlaskForm):
    """Creating a WTF class with inheritance"""
    email = StringField(label='Email')
    password = PasswordField(label='Password')
    submit = SubmitField(label="Submit")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    form = MyForm()
    return render_template("login.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
