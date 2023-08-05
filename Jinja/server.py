# Day 57 - Templating with Jinja

from flask import Flask, render_template
import random
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home_page():
    # In order to show a random number, we'll need to use kwargs of render_template()
    return render_template("index.html", rand_num=random.randint(1, 10), year=datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True)