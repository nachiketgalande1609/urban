from flask import Blueprint, session, jsonify, request, redirect, url_for
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Signup route
@user_bp.route('/signup', methods=['POST'])
def signup():
    from user.models import User
    user = User()
    return user.signup()

# Signout route
@user_bp.route('/signout')
def signout():
    from user.models import User
    user = User()
    return user.signout()

# Login route
@user_bp.route('/login', methods=['POST'])
def login():
    from user.models import User
    user = User()
    return user.login()

# Get user_id route
@user_bp.route('/get_user_id')
def get_user_id():
    user_id = session['user']['_id'] if 'user' in session else None
    return jsonify({'user_id': user_id})
    
# Password reset route
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
        return jsonify({"error": "Current password in incorrect"}), 401
