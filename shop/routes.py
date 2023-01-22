from shop import app
from flask import render_template
from shop.forms import RegisterForm
from shop.models import Product


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/shop')
def shop_page():
    products = Product.query.all()
    return render_template('shop.html', products=products)


@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)