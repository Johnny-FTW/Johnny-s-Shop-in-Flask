from flask_login import login_user, logout_user, login_required, current_user
from shop import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from shop.forms import RegisterForm, SignInForm, AddToCart, BuyNow, CancelOrder
from shop.models import Product, Customer, Password, OrderedProducts
from shop.services import show_order, show_total_price, cancel_order


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/shop', methods=['GET','POST'])
def shop_page():
    products = Product.query.all()
    orders = None
    add_form = AddToCart()
    buy_form = BuyNow()
    total_price = 0
    cancel_form = CancelOrder()
    if current_user.is_authenticated:
        if request.method == 'POST':
            if "product" in request.form:
                purchased_product = request.form.get('product')
                ordered_product = OrderedProducts(product_id=purchased_product, customer_id=current_user.id)
                db.session.add(ordered_product)
                db.session.commit()
                flash(f'Product was added to your order!', category='success')
                orders = show_order()
                total_price = show_total_price()
            elif "buy_now" in request.form:
                orders = show_order()
                total_price = show_total_price()
                if current_user.can_purchase(total_price):
                    current_user.budget -= total_price
                    db.session.commit()
                    flash(f'Thank you for order!', category='success')
                else:
                    flash(f'Not enough money.', category='info')
            elif "cancel_order" in request.form:
                cancel_order()
                flash(f'Your order was canceled.', category='info')
        else:
            total_price = show_total_price()
            orders = show_order()
    else:
        if add_form.is_submitted():
            flash('You need sign in first!', category='info')

    return render_template('shop.html', products=products, buy_form=buy_form, add_form=add_form,
                           total_price=total_price, orders=orders, cancel_form=cancel_form)


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








