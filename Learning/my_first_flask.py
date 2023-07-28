# yay, I started flask
# Use `flask run`  if using terminal for running

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!!!"

@app.route("/bye")
def bye():
    """This is gonna get triggerd if the user adds '/bye' into the end of the URL and hit enter"""
    return "Bye!"


if __name__ == "__main__":
    app.run()