from flask import Blueprint, jsonify, request
from models import db, Product

product_bp = Blueprint('products', __name__)

# Ruta para obtener todos los productos
@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

# Ruta para crear un producto
@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# Ruta para editar un producto
@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify(product.to_dict()), 200

# Ruta para eliminar un producto
@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
