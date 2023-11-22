from flask import Blueprint, render_template
# Create a Blueprint named 'user' with a URL prefix '/user'
product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/addproduct', methods=['POST'])
def addproduct():
    from product.models import Product
    product = Product()
    return product.addproduct()

@product_bp.route('/<product_id>')
def product_detail(product_id):
    from app import db
    from datetime import datetime, timedelta
    delivery_date = datetime.now() + timedelta(days=7)
    delivery_date_str = delivery_date.strftime("%a, %d %b")
    product = db.products.find_one({"_id": product_id})
    return render_template('product_detail.html', product=product, delivery_date=delivery_date_str)