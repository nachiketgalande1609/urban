from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200
    
    def signup(self):
        user = {
            "_id": uuid.uuid4().hex,                            # Generate unique id
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        # Check for existing user
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "User already exists"}), 400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup Failed"}), 400
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = db.users.find_one({"email": request.form.get('email')})
        if user:
            if pbkdf2_sha256.verify(request.form.get('password'), user['password']):
                return self.start_session(user)
            else:
                return jsonify({"error": "Invalid password"}), 401
        else:
            return jsonify({"error": "User not found. Please Sign up"}), 401