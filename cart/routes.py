from flask import Blueprint, request, jsonify

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# Add item to cart route
@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    from app import db
    if 'user_id' in request.form and 'product_id' in request.form:
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        size = request.form['size']

        cart_item = {
            'user_id': user_id,
            'product_id': product_id,
            'size': size
        }

        db.cart.insert_one(cart_item)
        
        return jsonify({"message": "Product added to cart successfully"}), 200
    else:
        return jsonify({"error": "Missing user ID or product ID"}), 400
    
# Remove item from cart route
@cart_bp.route('/remove_from_cart/<item_id>', methods=['POST'])
def remove_from_cart(item_id):
    from app import db
    if db.cart.delete_one({"product_id": item_id}):
        return jsonify({"message": "Product removed from cart successfully"}), 200
    else:
        return jsonify({"error": "Missing user ID or product ID"}), 400