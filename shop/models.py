from shop import db


class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=20), nullable=False)
    last_name = db.Column(db.String(length=20), nullable=False)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    address = db.Column(db.String(length=40), nullable=False)
    postcode = db.Column(db.String(length=20), nullable=False)
    country = db.Column(db.String(length=20), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=500)
    password = db.relationship('Password', backref='customer', uselist=False)


class Password(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String(length=60), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Product {self.name}'