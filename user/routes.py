from flask import Blueprint, session, jsonify, request, redirect, url_for
# Create a Blueprint named 'user' with a URL prefix '/user'
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/signup', methods=['POST'])
def signup():
    from user.models import User
    user = User()
    return user.signup()

@user_bp.route('/signout')
def signout():
    from user.models import User
    user = User()
    return user.signout()

@user_bp.route('/login', methods=['POST'])
def login():
    from user.models import User
    user = User()
    return user.login()

@user_bp.route('/get_user_id')
def get_user_id():
    user_id = session['user']['_id'] if 'user' in session else None
    return jsonify({'user_id': user_id})

@user_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    from app import db
    if 'user_id' in request.form and 'product_id' in request.form:
        user_id = request.form['user_id']
        product_id = request.form['product_id']

        cart_item = {
            'user_id': user_id,
            'product_id': product_id
        }

        db.cart.insert_one(cart_item)
        
        return jsonify({"message": "Product added to cart successfully"}), 200
    else:
        return jsonify({"error": "Missing user ID or product ID"}), 400
    
from bson.objectid import ObjectId

@user_bp.route('/remove_from_cart/<item_id>', methods=['POST'])
def remove_from_cart(item_id):
    from app import db
    if db.cart.delete_one({"product_id": item_id}):
        return jsonify({"message": "Product added to cart successfully"}), 200
    else:
        return jsonify({"error": "Missing user ID or product ID"}), 400