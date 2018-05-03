"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_form():
    """ Requests email and password"""

    # ask for email and password
    return render_template("homepage.html")


@app.route("/register", methods=["POST"])
def register_process():

    email = request.form.get("Email")

    password = request.form.get("Password")
    
    user = User.query.filter_by(email=email).first()

    if user:
        flash("Your account already exists!")
        
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("You have now been registered. Please log in!")

    return render_template("login.html")


@app.route("/login", methods=["GET"])
def log_in():

    # get email address 
    email = request.args.get("Email")

    # get password 
    password = request.args.get("Password")

    # query for email address 
    user = User.query.filter_by(email=email).first()

    if user:
    # check if email address matches password, log in, 
        if password == user.password:

            flash ("success!")
            session['user'] = user.user_id
            return redirect("/")
        else:
            flash("Password did not match. Please try again.")
            return render_template("login.html")
    else:
        flash("User doesn't exist. Please register.")
        return redirect("/")       
    




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
