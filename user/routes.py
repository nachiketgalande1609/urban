from flask import Blueprint
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