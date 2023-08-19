# Day 57 - Blog Capstone project
# Day 59 - Upgrading Blog
# Day 60 - Getting the HTML forms to work and send email to myself as a form has been correctly filled

from flask import Flask, render_template, request
import requests
import smtplib
from datetime import datetime
import config

app = Flask(__name__)

response = requests.get("https://api.npoint.io/079a621441e20cdc107d")
blogs = response.json()
year = datetime.now().year

def send_email(name, email, phone_number, msg):
    """Sends emails"""
    email_msg = "Subject:New Form Response\n\n" \
                f"Name: {name}\n" \
              f"Email: {email}\n" \
              f"Phone Number: {phone_number}\n" \
              f"Message: {msg}\n"
    with smtplib.SMTP("smtp.gmail.com") as conn:
        conn.starttls()
        conn.login(user=config.my_email, password=config.my_password)
        conn.sendmail(
            from_addr=config.my_email,
            to_addrs=config.send_email,
            msg=email_msg
        )


@app.route('/')
def home():
    return render_template("index.html", blogs=blogs, year=year)

@app.route("/post/<int:num>")
def post(num):
    title = blogs[num-1]["title"]
    body = blogs[num-1]["body"]
    subtitle = blogs[num-1]["subtitle"]
    date = blogs[num-1]["date"]
    id = blogs[num-1]["id"]
    return render_template("post.html", title=title, body=body, subtitle=subtitle, date=date, id=id, year=year)

@app.route("/about")
def about():
    return render_template("about.html", year=year)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    # h1_message indicates what should be shown in the h1 of '/contact' page depending on method (get or post)
    # I think this would be a better approach than adding 'if's in html file with Jinja
    if request.method == "GET":
        return render_template("contact.html", h1_message="Contact Me", year=year)
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        send_email(name=name, email=email, phone_number=phone, msg=message)
        return render_template("contact.html", h1_message="Successfully sent your message", year=year)


if __name__ == "__main__":
    app.run(debug=True)
