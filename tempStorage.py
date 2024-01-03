

 
#Manage users logging in and out
login_manager = LoginManager()
login_manager.init_app(app)




# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)



# Sign users up
@app.route('/register', methods=["GET", "POST"])
def register():
  # If the user made a POST request, create a new user
    if request.method == "POST":
        user = Users(firstname=request.form.get("firstname"),
                     lastname=request.form.get("lastname"),
                     username=request.form.get("username"),
                     email=request.form.get("email"),
                     password=request.form.get("password"))
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("create_account.html")