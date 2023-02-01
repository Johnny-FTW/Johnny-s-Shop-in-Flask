from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func

from shop import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from shop.forms import RegisterForm, SignInForm, AddToCart
from shop.models import Product, Customer, Password, OrderedProducts


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/shop', methods=['GET','POST'])
def shop_page():
    products = Product.query.all()
    form = AddToCart()

    if current_user.is_authenticated:
        orders = db.session.query(OrderedProducts.id, Product.name, Product.price)\
            .join(Product,Product.id == OrderedProducts.product_id, isouter=True).all()
        if request.method == 'POST':
            purchased_product = request.form.get('product')
            ordered_product = OrderedProducts(product_id=purchased_product, customer_id=current_user.id)
            db.session.add(ordered_product)
            db.session.commit()
            flash(f'Product was added to your order!', category='success' )
            orders = db.session.query(OrderedProducts.id, Product.name, Product.price)\
                .join(Product, Product.id == OrderedProducts.product_id, isouter=True).all()
        total_price = db.session.query(func.sum(Product.price)).filter(Product.id == OrderedProducts.product_id).one()
        return render_template('shop.html', products=products, form=form, orders=orders, total_price=total_price)
    else:
        if request.method == 'POST':
            flash('You need sign in first!', category='info')
    return render_template('shop.html', products=products, form=form)


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
        login_user(customer_to_create)
        flash('Account created successfully!', category='success')
        return redirect(url_for('shop_page'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Error:{err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
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
@login_required
def logout_page():
    logout_user()
    flash('You have been logget out!', category='info')
    return redirect(url_for('home_page'))








