from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_bcrypt import bcrypt, Bcrypt

'''
Setup
'''

# Create instance of a flask application, keep default folder name as "templates" and "static"
app = Flask(__name__, template_folder='templates', static_folder='static')

# Connect to and configure database
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "my_secret_key"

# Class for the users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

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

# signin.html
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        
        # Check for correct password 
        entered_pw = request.form.get("password")
        hashed_pw = user.password
        if bcrypt.check_password_hash(hashed_pw, entered_pw):
            login_user(user)
            return redirect(url_for("home"))
        #TODO tell user if they have entered incorrect password
        else:
            return("Password did not work :(")
        
    return render_template("signin.html")

# create_account.html
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        # If the user made a POST request, create a new user
        hashed_pw = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
        un = request.form.get("username")

        #TODO check if username is taken
        if (User.query.filter_by(username=request.form.get("username")).first()):
            return render_template("create_account.html")
        # If username if not taken
        user = User(firstname=request.form.get("firstname"),
                     lastname=request.form.get("lastname"),
                     username=un,
                     password=hashed_pw)
        # Add the user to the database and commit changes
        db.session.add(user)
        db.session.commit()

        # Redirect to login page
        return redirect(url_for("signin"))

    return render_template("create_account.html")

if (__name__ == '__main__'):
    app.run(debug=True)




'''
GEEKSFORGEEKS flask tutorial
https://www.geeksforgeeks.org/flask-tutorial/?ref=lbp

'''

#bingus