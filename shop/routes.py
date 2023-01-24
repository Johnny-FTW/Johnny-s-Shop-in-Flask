from shop import app, db
from flask import render_template, redirect, url_for, flash
from shop.forms import RegisterForm
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
        password_real = Password(value=form.password1.data, customer=customer_to_create)
        db.session.add(customer_to_create)
        db.session.add(password_real)
        db.session.commit()
        return redirect(url_for('shop_page'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Error:{err_msg}', category='danger')
    return render_template('register.html', form=form)