# This is a mini project of Day 55
# This is basically a number guessing game but on a website
# Random number range from 1 to 9 inclusive
"""This is how the program works
    1. First the program generate a random number
    2. When you enter the webpage it says to guess a random number and shows a gif
    3. The random number should be added to the end of the URL (/9)
    4. If the number is too high or low, the webpage shows it
    5. Else the number happens to be the correct number, then it says so and shows a gif
"""

import random
from flask import Flask

app = Flask(__name__)

rand_num = random.randint(1, 9)

@app.route("/")
def home_page():
    return "<h1>Guess a number between 1 and 9 inclusive</h1>" \
           "<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2Q1dWp0czIzcTh3M2xyNW40c2l4Z2hwZzU1M2s1NzRheW50dGxyNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xUn3CftPBajoflzROU/giphy-downsized-large.gif'>"

@app.route("/<int:guess>")
def guess_numer(guess):
    if guess == rand_num:
        return "<h2 style='color:green'>You got it correct!</h2>" \
               "<img src='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeHZ3bnl1NHJlZjhjanlhaHIyc2tqNGN5OWhobDZhbWprdzR2NnhkdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yy6hXyy2DsM5W/giphy.gif'>"
    elif guess < rand_num:
        return "<h2 style='color:red'>Too low!</h2>" \
               "<img src='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExd295azhxaXBpNW45Mzl2czMxZjk1cmFwa3ZpaGxlbnNwMHA3YzNucSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/URJyuwpBJLewEJMqXP/giphy.gif'>"
    else:
        return "<h2 style='color:purple'>Too high!</h2>" \
               "<img src='https://media4.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif?cid=ecf05e47uhqvco42y80s4kvpxjq85eoicstyi8fi1l2uo2t1&ep=v1_gifs_search&rid=giphy.gif&ct=g'>"


if __name__ == "__main__":
    app.run(debug=True)