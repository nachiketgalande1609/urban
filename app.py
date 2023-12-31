from flask import Flask, render_template, redirect, session, url_for, request, jsonify
from functools import wraps
from user.routes import user_bp
from cart.routes import cart_bp
from wishlist.routes import wishlist_bp
from product.routes import product_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import os

app = Flask(__name__)

# Register the user and product blueprint routes with the Flask app
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(wishlist_bp)


from dotenv import load_dotenv
load_dotenv()

app.secret_key = os.getenv('APP_SECRET_KEY')
password = os.getenv('DB_PASSWORD')
uri = os.getenv('DB_URI')

# MongoDB Configuration
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

# Check if user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)
        if session.get('logged_in') and session.get('is_admin'):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return decorated_function

def get_user_id():
    return session.get('user').get('_id')

# Login route
@app.route('/login/')
def login():
    return render_template('login.html')

# Signup route
@app.route('/signup/')
def signup():
    return render_template('signup.html')

# Add Product route
@app.route('/addproduct/')
@login_required
@admin_required # Give access to this page only if the user is an admin
def addproduct():
    return render_template('addproduct.html')

# Cart route
@app.route('/cart/')
@login_required
def cart():
    user_id = get_user_id()
    cart_with_product_details, total_price = get_cart_items(user_id)
    return render_template('cart.html', cart_items=cart_with_product_details, total_price=total_price)

# Wishlist route
@app.route('/wishlist/')
@login_required
def wishlist():
    user_id = get_user_id()
    wishlist_with_product_details = get_wishlist_items(user_id)
    return render_template('wishlist.html', wishlist_items=wishlist_with_product_details)

# Address route
@app.route('/address/', methods=['POST', 'GET'])
@login_required
def address():
    user_id = get_user_id()
    added_address = request.form.get('address')
    if added_address:
        db.users.update_one({'_id': user_id}, {'$set': {'address': added_address}})

    address = db.users.find_one({'_id': user_id}, {'_id':0, 'address':1})
    cart_with_product_details, total_price = get_cart_items(user_id)
    return render_template('address.html', address=address, cart_items=cart_with_product_details, total_price=total_price)

# Home route
@app.route('/home', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    from user.models import User
    from flask_paginate import Pagination, get_page_args
    user = User()
    selected_category = request.args.get('category')
    dropdown_selected_gender = request.args.get('gen')
    sort_order = request.args.get('sort')
    search_query = request.args.get('search')
    selected_colors = request.args.getlist('color')
    selected_genders = request.args.getlist('gender')
    selected_categories = request.args.getlist('categories')
    filters = {}
    if selected_genders:
        filters['gender'] = {'$in': selected_genders}
    if selected_colors:
        filters['colors'] = {'$in': selected_colors}
    if selected_categories:
        filters['category'] = {'$in': selected_categories}
    if dropdown_selected_gender:
        filters['gender'] = dropdown_selected_gender
    if search_query:
        filters['$or'] = [
            {'name': {'$regex': f'.*{search_query}.*', '$options': 'i'}},
            {'category': {'$regex': f'.*{search_query}.*', '$options': 'i'}}
        ]
    if selected_category:
        filters['category'] = selected_category
    else:
        selected_category=''
    products = db.products.find(filters)
    if sort_order == 'asc':
        products = products.sort("price", 1)
    elif sort_order == 'desc':
        products = products.sort("price", -1)

    product_count = db.products.count_documents(filters)  # Count documents after filters

    # Pagination setup
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    products = products.skip(offset).limit(per_page)

    pagination = Pagination(page=page, total=product_count, per_page=per_page, css_framework='bootstrap')

    return render_template('home.html', products=products, user=user, selected_category=selected_category,
                           product_count=product_count, search_query=search_query, pagination=pagination, 
                           selected_genders=selected_genders, selected_colors=selected_colors, selected_categories=selected_categories, filters=filters)

# Account route
@app.route('/account/')
@login_required
def account():
    user_id = get_user_id()
    user = db.users.find_one({'_id': user_id})
    order_history = db.orders.find({'user_id': user_id})
    order_history = order_history.sort("created_at", -1)

    formatted_order_history = []
    for order in order_history:
        order['created_at'] = order['created_at'].strftime("%a, %d %b %Y")  # Convert datetime to custom format
        formatted_order_history.append(order)

    return render_template('account.html', order_history=formatted_order_history, user=user)


# Get cart details for the current user
def get_cart_items(user_id):
    user_cart_items = db.cart.find({'user_id': user_id})
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

    return cart_with_product_details, total_price

def get_wishlist_items(user_id):
    user_wishlist_items = db.wishlist.find({'user_id': user_id})
    wishlist_with_product_details = []

    for item in user_wishlist_items:
        product_id = item.get('product_id')
        product_details = db.products.find_one({'_id': product_id}, {'name': 1, 'image_path': 1, 'price': 1, 'category': 1})
        if product_details:
            item['product_name'] = product_details.get('name')
            item['image_path'] = product_details.get('image_path')
            item['price'] = product_details.get('price')
            item['category'] = product_details.get('category')
            wishlist_with_product_details.append(item)
    return wishlist_with_product_details

# Insert order details into orders collection
def insert_order(user_id, order_number, product_ids, total_price, total_amount, cgst, sgst, delivery_date, address, cart_with_product_details):
    from datetime import datetime
    order = {
        "_id": uuid.uuid4().hex,
        "order_number": order_number,
        "user_id": user_id,
        "total_price": total_price,
        "total_amount": total_amount,
        "cgst": cgst,
        "sgst": sgst,
        "delivery_date": delivery_date,
        "address": address,
        "products": [],
        "created_at": datetime.now()
    }
    db.cart.delete_many({"user_id": user_id})
    
    # Fetch product details including image_path from the products collection
    for product_info in cart_with_product_details:
        product_id = product_info.get('product_id')
        product_details = db.products.find_one({'_id': product_id})
        if product_details:
            product = {
                "product_id": product_id,
                "image_path": product_details.get('image_path'),
                "product_name": product_details.get('name'),
                "price": product_details.get('price'),
                "category": product_details.get('category'),
                "size": product_info.get('size')  # Access 'size' from the current product_info dictionary
            }
            order["products"].append(product)

    # Insert order into the database
    db.orders.insert_one(order)
    return None

# Download invoice pdf
@app.route('/invoice')
def invoice():
    import pdfkit
    from flask import make_response
    from datetime import datetime, timedelta
    user_id = get_user_id()
    address = db.users.find_one({'_id': user_id}, {'_id': 0, 'address': 1})
    cart_with_product_details, total_price = get_cart_items(user_id)
    order_number = str(uuid.uuid4().int)[:8]
    delivery_date = datetime.now() + timedelta(days=7)
    delivery_date_str = delivery_date.strftime('%Y-%m-%d')
    
    cgst = total_price * 2.5 / 100
    sgst = total_price * 2.5 / 100
    total_amount = total_price + cgst + sgst

    product_ids = [item.get('product_id', ) for item in cart_with_product_details]
    insert_order(user_id, order_number, product_ids, total_price, total_amount, cgst, sgst, delivery_date_str, address, cart_with_product_details)
    
    rendered_html = render_template('invoice.html', cart_items=cart_with_product_details, total_price=total_price,
                                    total_amount=total_amount, cgst=cgst, sgst=sgst, address=address,
                                    order_number=order_number, delivery_date=delivery_date_str)

    config = pdfkit.configuration(wkhtmltopdf='./wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=invoice.pdf'

    return response

# Route for dashboard page
@app.route('/dashboard/')
@login_required
@admin_required
def dashboard():
    users = db.users.find()
    products = db.products.find()
    orders = db.orders.find()
    user_count = len(list(users))
    product_count = len(list(products))
    order_count = len(list(orders))

    # Revenue by category chart /////////////////////////////////////////////////////////////////
    revenue_by_category = db.orders.aggregate([
        {"$unwind": "$products"},
        {"$group": {"_id": "$products.category", "totalRevenue": {"$sum": "$products.price"}}}
    ])
    categories = []
    revenues = []
    for item in revenue_by_category:
        categories.append(item['_id'])
        revenues.append(item['totalRevenue'])

    if not categories or not revenues:
        return "No data available for the pie chart"
    # Revenue by category chart /////////////////////////////////////////////////////////////////

    return render_template('dashboard.html', user_count=user_count, product_count=product_count,
                           order_count=order_count, categories=categories, revenues=revenues)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(debug=True)