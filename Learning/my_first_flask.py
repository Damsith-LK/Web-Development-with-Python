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

# We can use variables in this <way>
@app.route("/user/<username>")
def greeting(username):
    """The webpage would show whatever the username that was typed in after '/user/' """
    return f"What's going on, {username}?"


# Also, we can specify the data type of the variable
@app.route("/user/<username>/<int:number>")
def lucky_number(username, number):
    return f"{username}, your lucky number is {number}"


if __name__ == "__main__":
    app.run(debug=True)  # If debug=True, we will be able to debug the webpage we created live