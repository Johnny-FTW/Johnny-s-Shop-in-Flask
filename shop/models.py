from shop import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(customer_id):
    return Customer.query.get(int(customer_id))


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=20), nullable=False)
    last_name = db.Column(db.String(length=20), nullable=False)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    address = db.Column(db.String(length=40), nullable=False)
    postcode = db.Column(db.String(length=20), nullable=False)
    country = db.Column(db.String(length=20), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=500)
    password = db.relationship('Password', backref='customer', uselist=False)
    ordered_products = db.relationship('OrderedProducts', backref='product_c', lazy=True)


class Password(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(length=60), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def check_password(self, password):
        return bcrypt.check_password_hash(self.value, password)


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    ordered_products = db.relationship('OrderedProducts', backref='product_p', lazy=True)

    def __repr__(self):
        return f'Product:{self.name}'


class OrderedProducts(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
