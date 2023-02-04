from flask_login import current_user
from sqlalchemy import func
from shop import db
from shop.models import OrderedProducts, Product


def show_order():
    return db.session.query(OrderedProducts.customer_id, Product.name, Product.price) \
        .filter_by(customer_id=current_user.id) \
        .join(Product, Product.id == OrderedProducts.product_id, isouter=True).all()


def show_total_price():
    total_price = db.session.query(func.sum(Product.price)).filter(Product.id == OrderedProducts.product_id) \
        .join(OrderedProducts, OrderedProducts.customer_id == current_user.id, isouter=True).one()
    return total_price[0]


def cancel_order():
    products_to_delete = OrderedProducts.query.filter_by(customer_id=current_user.id).all()
    for product in products_to_delete:
        db.session.delete(product)
        db.session.commit()
