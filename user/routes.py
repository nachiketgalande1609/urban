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
    
    
@user_bp.route('/change_password', methods=['POST'])
def change_password():
    from app import db
    from passlib.hash import pbkdf2_sha256

    current_password = request.form['currentPassword']
    new_password = request.form['newPassword']
    current_user_id = session.get('user').get('_id')
    
    current_user = db.users.find_one({"_id": current_user_id})
    if current_user and pbkdf2_sha256.verify(current_password, current_user['password']):
        print("Passwords match")
        new_hashed_password = pbkdf2_sha256.hash(new_password)
        db.users.update_one({"_id": current_user_id}, {"$set": {"password": new_hashed_password}})
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        print("Passwords do not match")
        return jsonify({"error": "Passwords do not match"}), 401
