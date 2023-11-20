from flask import Flask, render_template, redirect, session, url_for, request
from functools import wraps
from user.routes import user_bp
from product.routes import product_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
app.secret_key = "njSND78adhsbasb7has7hd7aHCaiu98hsvvu"

# MongoDB Configuration
password = "Mazaappu@1"
uri = "mongodb://localhost:27017/"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.urban

# Check if user is logged in
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/')
    return wrap

# Register the user and product blueprint routes with the Flask app
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)

# Home route
@app.route('/')
def home():
    from user.models import User
    user = User()
    selected_category = request.args.get('category')
    selected_gender = request.args.get('gender')
    sort_order = request.args.get('sort')

    if selected_category:
        products = db.products.find({"category": selected_category, "gender": selected_gender})
    else:
        products = db.products.find()

    if sort_order == 'asc':
        products = products.sort("price", 1)
    elif sort_order == 'desc':
        products = products.sort("price", -1)

    if selected_category==None:
        selected_category=''

    product_count = len(list(products))
    products.rewind()

    return render_template('home.html', products=products, user=user, selected_category=selected_category, product_count=product_count)

# Login route
@app.route('/login/')
def login():
    return render_template('login.html')

# Signup route
@app.route('/signup/')
def signup():
    return render_template('signup.html')

# Account route
@app.route('/account/')
@login_required
def account():
    return render_template('account.html')

# Add Product route
@app.route('/addproduct/')
@login_required
def addproduct():
    return render_template('addproduct.html')

# Cart route
@app.route('/cart/')
@login_required
def cart():
    user_id = session.get('user').get('_id')  # Get the current user's ID from the session
    user_cart_items = db.cart.find({'user_id': user_id})  # Fetch cart items for the current user
    cart_with_product_details = []
    total_price = 0

    for item in user_cart_items:
        product_id = item.get('product_id')
        product_details = db.products.find_one({'_id': product_id}, {'name': 1, 'image_path': 1, 'price': 1})
        if product_details:
            item['product_name'] = product_details.get('name')
            item['image_path'] = product_details.get('image_path')
            item['price'] = product_details.get('price')
            cart_with_product_details.append(item)
            total_price += product_details.get('price', 0)
    return render_template('cart.html', cart_items=cart_with_product_details, total_price=total_price)


# Run the Flask application if this script is executed directly
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True)