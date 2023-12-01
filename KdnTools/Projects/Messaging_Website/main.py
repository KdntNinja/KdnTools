from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    messages_sent = db.relationship('Message', backref='author', lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Add user registration logic here
        pass
    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add user login logic here
        pass
    return render_template('login.html')


@app.route("/send_message", methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        # Add message sending logic here
        pass
    return render_template('send_message.html')


@app.route("/inbox")
def inbox():
    # Add message receiving logic here
    return render_template('inbox.html')


@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
