from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

import os
from werkzeug.utils import secure_filename


class Product:
    def addproduct(self):
        product = {
            "_id": uuid.uuid4().hex,                            # Generate unique id
            "name": request.form.get('name'),
            "price": request.form.get('price'),
        }

        image_file = request.files['image']

        # Save the image to a specific directory
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join('static', 'product_images', image_filename)
            image_file.save(image_path)

        product['image_path'] = image_path

        if db.products.insert_one(product):
            return jsonify(product), 200

        return jsonify({"error": "insert Failed"}), 400