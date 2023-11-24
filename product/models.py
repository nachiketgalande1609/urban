from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

import os
from werkzeug.utils import secure_filename


class Product:
    def addproduct(self):
        product = {
            "_id": uuid.uuid4().hex,  # Generate unique id
            "name": request.form.get('name'),
            "price": float(request.form.get('price')),
            "category": request.form.get('category'),
            "gender": request.form.get('gender'),
        }
        # Handle multiple images
        images = []


        display_image_file = request.files['display_image']
        # Save the image to a specific directory
        if display_image_file:
            display_image_filename = secure_filename(display_image_file.filename)
            display_image_path = os.path.join('static', 'product_images', display_image_filename)
            display_image_file.save(display_image_path)
        
        product['image_path'] = display_image_path

        for image_file in request.files.getlist('images[]'):
            if image_file:
                image_filename = secure_filename(image_file.filename)
                print(image_filename)
                image_path = os.path.join('static', 'product_images', image_filename)
                image_file.save(image_path)
                images.append(image_path)

        product['images'] = images

        if db.products.insert_one(product):
            return jsonify(product), 200

        return jsonify({"error": "insert Failed"}), 400
