from flask import Flask, render_template, redirect, session
from functools import wraps
from user.routes import user_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
app.secret_key = "njSND78adhsbasb7has7hd7aHCaiu98hsvvu"

# MongoDB Configuration
password = "Mazaappu@1"
uri = "mongodb+srv://nachiketgalande:Mazaappu%401@login.ohobhje.mongodb.net/"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.serenityshops

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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/account/')
@login_required
def account():
    return render_template('account.html')

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)