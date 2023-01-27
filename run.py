from shop import app , db
from shop.models import Product

if __name__ == "__main__":
    with app.app_context():
        #db.drop_all()
        db.create_all()

    app.run(debug=False)

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