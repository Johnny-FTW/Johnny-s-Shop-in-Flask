from flask import Flask, render_template ,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:komojini@localhost:5432/johnnys_shop' #care heslo
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Product {self.name}'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/shop')
def shop_page():
    products = Product.query.all()
    return render_template('shop.html', products=products)


if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        print(Product.query.all())

    app.run(debug=True)



# i1 = Product(name='Banana', price=10, description='This is banana')
# db.session.add(i1)
# i2 = Product(name='Apple', price=20, description='This is apple')
# db.session.add(i2)
# i3 = Product(name='Cherry', price=30, description='This is cherry')
# db.session.add(i3)
# i4 = Product(name='Strawberry', price=15, description='This is strawberry')
# db.session.add(i4)
# i5 = Product(name='Pineapple', price=18, description='This is pineapple')
# db.session.add(i5)
# db.session.commit()