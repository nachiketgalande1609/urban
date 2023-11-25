from flask import Blueprint, jsonify, request
wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

# Add item to wishlist on button click
@wishlist_bp.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    from app import db
    if 'user_id' in request.form and 'product_id' in request.form:
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        existing_item = db.wishlist.find_one({'user_id': user_id, 'product_id': product_id})
        if existing_item:
            return jsonify({"message": "Product already exists in wishlist"}), 400
        else:
            wishlist_item = {
                'user_id': user_id,
                'product_id': product_id,
            }
            db.wishlist.insert_one(wishlist_item)
            return jsonify({"message": "Product added to wishlist successfully"}), 200
    else:
        return jsonify({"error": "Missing user ID or product ID"}), 400
    
# Remove item from wishlist
@wishlist_bp.route('/remove_from_wishlist/<item_id>', methods=['POST'])
def remove_from_wishlist(item_id):
    from app import db
    if db.wishlist.delete_one({"product_id": item_id}):
        return jsonify({"message": "Product deleted from wishlist successfully"}), 200
    else:
        return jsonify({"error": "Missing user ID or product ID"}), 400