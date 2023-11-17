from flask import Flask, render_template, redirect, session, url_for
from functools import wraps
from user.routes import user_bp
from product.routes import product_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
app.secret_key = "njSND78adhsbasb7has7hd7aHCaiu98hsvvu"

# MongoDB Configuration
password = "Mazaappu@1"
uri = "mongodb+srv://nachiketgalande:Mazaappu%401@urban.0mj15jx.mongodb.net/"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.urban

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/')
    return wrap

# Register the user blueprint with the Flask app
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)

@app.route('/')
def home():
    products = db.products.find()  # Fetch products from the database
    return render_template('home.html', products=products)

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/signup/')
def signup():
    return render_template('signup.html')

@app.route('/account/')
@login_required
def account():
    return render_template('account.html')

@app.route('/addproduct/')
@login_required
def addproduct():
    return render_template('addproduct.html')

@app.route('/cart/')
@login_required
def cart():
    return render_template('cart.html')

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)