from flask import Flask, json, request, redirect, url_for, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import bcrypt, Bcrypt
import validators

'''
Setup
'''

# Create instance of a flask application, keep default folder name as "templates" and "static"
app = Flask(__name__, template_folder='templates', static_folder='static')

# Connect to and configure database
db = SQLAlchemy()
app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

# Session handling
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Class for the users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Class for the lessons uploaded by users
class Lesson(db.Model):
    __table__name = 'lessons'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False)
    language = db.Column(db.String(),nullable = False)
    format = db.Column(db.String(), nullable = False)
    uploaded_by = db.Column(db.String(25), nullable=False)
    link = db.Column(db.String(), nullable=False)

    def __init__(self,name,language,format, uploaded_by, link):
        self.name = name
        self.language = language
        self.format = format
        self.uploaded_by = uploaded_by
        self.link = link

# Initialize database in context of app
db.init_app(app)

with app.app_context():
    db.create_all()

# Add login manager and user loader, enable password hashing
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

'''
Routing and page management
'''

# home.html
@app.route('/')
def home():
    return render_template("home.html")

# Update data displayed based on user preferences
@app.route('/filter', methods=['POST'])
def filter():
    filters = request.get_json()
    print(filters)
    langauge = filters["language"]
    format = filters["format"]
    # TODO apply filters
    return redirect(url_for("home"))

# Upload lesson a user has found
@app.route('/upload')
def upload():
    new_lesson = request.get_json()
    print(new_lesson)
    name = new_lesson["name"]
    link = new_lesson["link"]
    language = new_lesson["language"]
    format = new_lesson["format"]
    uploaded_by = session["username"]
    
    return redirect(url_for("dashboard"))

# dashboard for logged in users
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        name = request.form.get("name")
        link = request.form.get("link")
        language = request.form.get("language")
        format = request.form.get("format")
        uploaded_by = session["username"]
        validation = validators.url(link)
        if validation:
            entry = Lesson(name,language,format, uploaded_by, link)
            print(entry.name)
            flash("Addition successful. Thank you for contributing!")
            flash_color = "green"
        elif not validation:
            flash("Addition unsuccessful. Invalid or unsafe URL")
            flash_color = "red"
        return render_template("dashboard.html", flash_color=flash_color)

# logout
@app.route('/logout')
def logout():
    session["name"] = None
    session["username"] = None
    return redirect(url_for("home"))

# login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Check for valid username
        if (not User.query.filter_by(username=request.form.get("username")).first()):
            flash("Username does not exist. Please login with your username and password")

        else:
            user = User.query.filter_by(
            username=request.form.get("username")).first()
            # Check for correct password 
            entered_pw = request.form.get("password")
            hashed_pw = user.password
            if bcrypt.check_password_hash(hashed_pw, entered_pw):
                session["name"] = user.firstname
                session["username"] = user.username
                return redirect(url_for("home"))
            else:
                flash("Incorrect password!")
        
    return render_template("login.html")

# create_account.html
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        # If the user made a POST request, create a new user
        hashed_pw = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
        un = request.form.get("username")

        # check if username is taken
        if (User.query.filter_by(username=request.form.get("username")).first()):
            flash("Username already exists. Please choose a different username")
            return redirect(url_for("create_account"))
        
        # If username if not taken
        else:
            user = User(firstname=request.form.get("firstname"),
                     lastname=request.form.get("lastname"),
                     username=un,
                     password=hashed_pw)
            # Add the user to the database and commit changes
            db.session.add(user)
            db.session.commit()
            # Log user in and redirect to login page
            session["name"] = user.firstname
            session["username"] = user.username
            return redirect(url_for("home"))

    return render_template("create_account.html")

if (__name__ == '__main__'):
    app.run(debug=True)




'''
MAIN RESOURCES USED
https://www.youtube.com/watch?v=71EU8gnZqZQ
https://www.geeksforgeeks.org/flask-tutorial/?ref=lbp
https://www.geeksforgeeks.org/profile-application-using-python-flask-and-mysql/
https://www.shiksha.com/online-courses/articles/python-filter-everything-you-need-to-know/#:~:text=Example%201%3A%20Filtering%20a%20list%20of%20numbers&text=In%20this%20example%2C%20we%20use,with%20the%20list%20of%20numbers.
https://www.geeksforgeeks.org/how-to-implement-filtering-sorting-and-pagination-in-flask/
'''

#bingus