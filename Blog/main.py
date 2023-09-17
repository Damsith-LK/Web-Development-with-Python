import datetime

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)
ckeditor = CKEditor(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

# CONFIGURE WTFORM
class NewPostForm(FlaskForm):
    """Form for creating new blog posts.
    Use in add_new_post()"""
    title = StringField(label="Blog Post Title", validators=[DataRequired(), Length(max=60)])
    subtitle = StringField(label="Subtitle", validators=[DataRequired()])
    name = StringField(label="Your Name", validators=[DataRequired()])
    img_url = StringField(label="Blog Image URL", validators=[DataRequired(), URL()])
    content = CKEditorField(label="Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="SUBMIT POST", render_kw={'style': 'margin: 15px;'})

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # Query the database for all the posts. Convert the data to a python list
    posts = db.session.execute(db.select(BlogPost).order_by(BlogPost.id)).scalars().all()
    return render_template("index.html", all_posts=posts)

# Add a route so that you can click on individual posts
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# Add_new_post() to create a new blog post
@app.route("/new-post", methods=["POST", "GET"])
def add_new_post():
    new_blog_post_form = NewPostForm()
    if new_blog_post_form.validate_on_submit():
        title = new_blog_post_form.title.data
        subtitle = new_blog_post_form.subtitle.data
        name = new_blog_post_form.name.data
        img_url = new_blog_post_form.img_url.data
        content = new_blog_post_form.content.data
        date = datetime.datetime.now().strftime('%B %d, %Y')
        # Creating new entry in DB
        new_post = BlogPost(
            title=title,
            subtitle=subtitle,
            author=name,
            img_url=img_url,
            body=content,
            date=date
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=new_blog_post_form, is_edit=False)

# TODO: edit_post() to change an existing blog post
@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    return render_template('make-post.html', is_edit=True)

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
