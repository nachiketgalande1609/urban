from flask import Blueprint, render_template
# Create a Blueprint named 'user' with a URL prefix '/user'
product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/addproduct', methods=['POST'])
def addproduct():
    from product.models import Product
    product = Product()
    return product.addproduct()