from flask import Flask, render_template, redirect, session
from models import User, Feedback, db, connect_db
from forms import RegisterUser, LoginForm, FeedbackForm, DeleteForm
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
        # db.drop_all()
        db.create_all()


@app.route('/')
def show_homepage():
    if "username" not in session:
        return redirect('/login')
    else:
        username = session['username']
        return redirect(f'/users/{username}')



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
        feedback = Feedback.query.all()  
        return render_template("show.html", user=user, feedback=feedback)
    


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Deletes user from table and logs you out. Redirects to login page."""

    if "username" not in session or username != session['username']:
        return render_template("noshow.html")

    user = User.query.filter_by(username=username).first()
    
    Feedback.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect('/login')        
        
@app.route('/logout')
def logout():
    """Log out route."""

    session.pop("username")
    return redirect("/login")



@app.route('/feedback/<feedback_id>')
def show_feedback_page(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    return render_template('showfeedback.html', feedback=feedback)



@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.user.username != session['username']:
        return render_template('noshow.html')

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.user.username}")
    

    



@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def show_feedback_update_page(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    
    if 'username' not in session or feedback.user.username != session['username']:
        return render_template('noshow.html')
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        
        return redirect(f'/users/{feedback.user.username}')
    else:
        return render_template('updatefeedback.html', form=form, feedback=feedback)



@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def new_feedback(username):
    """Show new feedback form & handle adding feedback"""

    if "username" not in session or username != session['username']:
        return render_template("noshow.html")
    
    form = FeedbackForm()
    user = User.query.filter_by(username=username).first() 

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        

        feedback = Feedback(title=title, content=content, user_id=user.id)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{user.username}')
    
    else:
        return render_template("newfeedback.html", form=form, user=user)

if __name__ == '__main__':
    app.run(debug=True)