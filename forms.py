from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Optional, Email

class AddUser(FlaskForm):
    """Form for adding users"""
    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    email = StringField("E-Mail Address", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])