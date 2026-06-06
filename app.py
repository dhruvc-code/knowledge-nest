from flask import Flask, render_template, request
import csv
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

ADMIN_EMAIL = "youradmin@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "yourgmail@gmail.com"
SENDER_PASSWORD = "your_app_password"


def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email Error:", e)


if not os.path.exists("students.csv"):
    with open("students.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Name",
            "Phone",
            "Email",
            "Age",
            "Interest",
            "Date",
            "Status"
        ])


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/course")
def course():
    return render_template("course.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        age = request.form["age"]
        interest = request.form["interest"]
        status = request.form["status"]

        with open("students.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                name,
                phone,
                email,
                age,
                interest,
                datetime.now().strftime("%d-%m-%Y %H:%M"),
                status
            ])

        return """
        <h2>Registration Successful</h2>
        <a href='/'>Back Home</a>
        """

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
