from flask import Flask, render_template, redirect, session
from models import User, db, connect_db
from forms import RegisterUser, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedbackapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



connect_db(app)

with app.app_context():
        db.drop_all()
        db.create_all()


@app.route('/')
def show_homepage():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_user():
    """User registration form; handle registration"""
    
    form = RegisterUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username

        return redirect(f'/users/{user.username}')
    else:
        return render_template('register.html', form=form)
    
@app.route('/login', methods=['GET','POST'])
def login():
    """User login form; handle login"""
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template('login.html', form=form)

    else:
        return render_template('login.html', form=form)
    
@app.route('/users/<username>')
def show_user(username): 
    """Shows page after users are authenticated"""
    if "username" not in session or username != session['username']:
        return render_template("noshow.html")
    
    else:
        user = User.query.filter_by(username=username).first()   
        return render_template("show.html", user=user)
        
        
@app.route('/logout')
def logout():
    """Log out route."""

    session.pop("username")
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)