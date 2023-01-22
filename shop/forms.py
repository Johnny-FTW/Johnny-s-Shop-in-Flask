from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    first_name = StringField(label='First Name:')
    last_name = StringField(label='Last Name:')
    email = StringField(label='Email:')
    address = StringField(label='Address:')
    postcode = StringField(label='Postcode:')
    country = StringField(label='Country:')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Create Account')