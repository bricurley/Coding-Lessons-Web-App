from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

# Create instance of a flask application
app = Flask(__name__)

# Connect to and configure database
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "my_secret_key"

# Class for the users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(35), nullable=False)
    lastname = db.Column(db.String(35), nullable=False)
    username = db.Column(db.String(35), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

db.init_app(app)

with app.app_context():
    db.create_all()

# Routing/page management
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/create_account')
def create_account():
    return render_template("create_account.html")

if (__name__ == '__main__'):
    app.run(debug=True)