from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
#from flask_wtf import wtforms
#from wtforms import StringField, PasswordField, SubmitField
#from wtforms.validators import InputRequired, Length, ValidationError

# Create instance of a flask application
app = Flask(__name__)

# Connect to and configure database
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "my_secret_key"

# Class for the users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(35), nullable=False)
    lastname = db.Column(db.String(35), nullable=False)
    username = db.Column(db.String(35), unique=True, nullable=False)
    password = db.Column(db.String(35), nullable=False)

db.init_app(app)

with app.app_context():
    db.create_all()

'''
# Allow users to register
class RegistrationForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min = 1, max=35)]),
    render_kw = {"placeholder": "Enter your first name"}

    lastname = StringField(validators=[InputRequired(), Length(min = 1, max=35)]),
    render_kw = {"placeholder": "Enter your last name"}

    username = StringField(validators=[InputRequired(), Length(min = 1, max=35)]),
    render_kw = {"placeholder": "Create a username"}

    firstname = StringField(validators=[InputRequired(), Length(min = 1, max=35)]),
    render_kw = {"placeholder": "Create a password"}

'''

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