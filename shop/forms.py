from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    first_name = StringField(label='name')
    last_name = StringField(label='surname')
    email = StringField(label='email')
    address = StringField(label='address')
    postcode = StringField(label='postcode')
    country = StringField(label='country')
    password1 = PasswordField(label='password1')
    password2 = PasswordField(label='password2')
    submit = SubmitField(label='submit')