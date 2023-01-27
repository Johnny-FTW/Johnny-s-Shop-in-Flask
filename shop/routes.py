from flask_login import login_user, logout_user
from shop import app, db, bcrypt
from flask import render_template, redirect, url_for, flash
from shop.forms import RegisterForm, SignInForm
from shop.models import Product, Customer, Password


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/shop')
def shop_page():
    products = Product.query.all()
    return render_template('shop.html', products=products)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        customer_to_create = Customer(first_name=form.first_name.data,
                                      last_name=form.last_name.data,
                                      email=form.email.data,
                                      address=form.address.data,
                                      postcode=form.postcode.data,
                                      country=form.country.data)
        password_hash = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        password_hashed = Password(value=password_hash, customer=customer_to_create)
        db.session.add(customer_to_create)
        db.session.add(password_hashed)
        db.session.commit()
        return redirect(url_for('shop_page'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Error:{err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/sign_in', methods=['GET','POST'])
def sign_in_page():
    form = SignInForm()
    if form.validate_on_submit():
        attempted_user = Customer.query.filter_by(email=form.email.data).first()
        if attempted_user:
            password = Password.query.filter_by(customer_id=attempted_user.id).first()
            if password.check_password(password=form.password.data):
                login_user(attempted_user)
                flash('You are logged in!', category='success')
                return redirect(url_for('shop_page'))
            else:
                flash('Wrong password.', category='danger')
        else:
            flash('Email does not exists.', category='danger')
    return render_template('sign_in.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logget out!', category='info')
    return redirect(url_for('home_page'))





