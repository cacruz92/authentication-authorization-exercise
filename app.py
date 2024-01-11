from flask import Flask, render_template, redirect, session, flash
from models import User, db, connect_db
from forms import RegisterUser
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

        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        
        db.session.add(new_user)
        db.session.commit()

        flash(f'Added {username}!', 'success')
        return redirect('/')
    else:
        return render_template('register.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)