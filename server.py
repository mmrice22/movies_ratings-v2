"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

#this throws errors when a variable is undefined, otherwise no error
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route('/movies')
def all_movies():
    """View all movies"""

    # use the function get_movies() from the crud.py and save it to the variable movies
    movies = crud.get_movies()

    return render_template('all_movies.html', movies = movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie = movie)


@app.route('/users', methods=['POST'])
def register_user():
    """Create a new uesr."""
    new_email = request.form.get('email')
    new_password = request.form.get('password')

     # if email exists, flash message to say you can't create an account 
     # if it doens't, create new user flash message telling it created successfully

    user = crud.get_user_by_email(new_email)

    if user:
        flash("Can't create an account with that email. Try again.")
    else: 
        crud.create_user(new_email, new_password)
        flash('Account created. Please log in.')
    
    return redirect('/')


@app.route('/login', methods=['POST'])
def login_user():
    user_email = request.form.get('email')
    user_password = request.form.get('password') 

    user_id = crud.user_id_if_match(password)
    session['Current User'] = user_id

    flash('Logged in!')
    
    redirect('/')


@app.route('/users')
def all_users():
    """View all users"""

    users = crud.get_user()

    return render_template('users.html', users = users)


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show users info based on the specified user_id"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_profile.html', user = user) 




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
