from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from shop.models import Customer


class RegisterForm(FlaskForm):

    def validate_email(self, email_to_check):
        customer = Customer.query.filter_by(email=email_to_check.data).first()
        if customer:
            raise ValidationError('Email already exists!')

    first_name = StringField(label='First Name:', validators=[Length(min=2, max=20), DataRequired()])
    last_name = StringField(label='Last Name:', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    address = StringField(label='Address:', validators=[Length(min=5, max=30), DataRequired()])
    postcode = StringField(label='Postcode:', validators=[Length(min=2, max=40), DataRequired()])
    country = StringField(label='Country:', validators=[Length(min=2, max=20), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class SignInForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')