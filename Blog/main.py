# Day 57 - Blog Capstone project
# Successfully completed it

from flask import Flask, render_template
from post import Post

app = Flask(__name__)
post = Post()
blogs = post.get_blogs()

@app.route('/')
def home():
    return render_template("index.html", blogs=blogs)

@app.route("/post/<int:num>")
def post(num):
    title = blogs[num-1]["title"]
    body = blogs[num-1]["body"]
    subtitle = blogs[num-1]["subtitle"]
    return render_template("post.html", title=title, body=body, subtitle=subtitle)


if __name__ == "__main__":
    app.run(debug=True)
