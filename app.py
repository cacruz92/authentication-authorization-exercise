from flask import Flask, render_template, redirect, session, flash

app = Flask(__name__)


# Make routes for the following:

# **GET */ :*** Redirect to /register.

@app.route('/')
def show_homepage():
    return redirect('/register')

@app.route('/register')
def show_register_form():
    return render_template('registerform.html')

# **GET */register :*** Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name. Make sure you are using WTForms and that your password input hides the characters that the user is typing!

# **POST */register :*** Process the registration form by adding a new user. Then redirect to ***/secret***

# **GET */login :*** Show a form that when submitted will login a user. This form should accept a username and a password. Make sure you are using WTForms and that your password input hides the characters that the user is typing!

# **POST */login :*** Process the login form, ensuring the user is authenticated and going to ***/secret*** if so.

# **GET */secret :*** Return the text “You made it!” (don’t worry, we’ll get rid of this soon)



if __name__ == '__main__':
    app.run(debug=True)