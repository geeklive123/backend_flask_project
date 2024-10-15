import os
import uuid
from flask import Blueprint, request, jsonify
from models import Product, Categoria  # Importa los modelos
from database import db  # Importa 'db' desde 'database.py'

product_bp = Blueprint('products', __name__)
upload_folder = 'uploads' 



@product_bp.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = Categoria.query.all()
        return jsonify([{'id': categoria.id, 'nombre': categoria.nombre} for categoria in categorias]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

        
# Ruta para obtener todos los productos
@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

# Ruta para obtener un producto por ID
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(product.to_dict()), 200

# Ruta para agregar un nuevo producto
@product_bp.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    nombre = request.form.get('nombre_producto')
    estado = request.form.get('estado_producto')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    categoria_id = request.form.get('categoria_id')
    departamento = request.form.get('departamento')
    numero_celular = request.form.get('numero_celular')
    imagen_url = request.files.get('imagen_url')  # Cambia para obtener el archivo

    if not all([nombre, estado, descripcion, precio, categoria_id, departamento, numero_celular, imagen_url]):
        return jsonify({"error": "Faltan datos"}), 400

    # Guarda la imagen
    imagen_path = os.path.join(upload_folder, imagen_url.filename)
    imagen_url.save(imagen_path)

    # Guarda la ruta de acceso pública
    public_imagen_url = f'/uploads/{imagen_url.filename}'
    nuevo_producto = Product(
        nombre_producto=nombre,
        estado_producto=estado,
        descripcion=descripcion,
        precio=float(precio),
        categoria_id=int(categoria_id),
        departamento=departamento,
        numero_celular=numero_celular,
        imagen_url=public_imagen_url  # Guarda la URL pública
    )
    
    db.session.add(nuevo_producto)
    db.session.commit()

    return jsonify({"mensaje": "Producto agregado exitosamente"}), 201

# Ruta para actualizar un producto por ID
@product_bp.route('/<int:product_id>', methods=['PUT'])
def actualizar_producto(product_id):
    try:
        print(f"Attempting to update product with ID: {product_id}")
        product = Product.query.get(product_id)
        if product is None:
            print(f"Product with ID {product_id} not found.")
            return jsonify({"error": "Producto no encontrado"}), 404

        # Procesa la solicitud para obtener datos
        nombre = request.form.get('nombre_producto')
        estado = request.form.get('estado_producto')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        categoria_id = request.form.get('categoria_id')
        departamento = request.form.get('departamento')
        numero_celular = request.form.get('numero_celular')
        imagen_file = request.files.get('imagen_url')

        # Log received data
        print(f"Received data: nombre={nombre}, estado={estado}, descripcion={descripcion}, precio={precio}, categoria_id={categoria_id}, departamento={departamento}, numero_celular={numero_celular}")

        # Actualiza los atributos del producto
        if nombre:
            product.nombre_producto = nombre
        if estado:
            product.estado_producto = estado
        if descripcion:
            product.descripcion = descripcion
        if precio:
            try:
                product.precio = float(precio)
            except ValueError:
                return jsonify({"error": "Precio inválido"}), 400
        if categoria_id:
            product.categoria_id = int(categoria_id)
        if departamento:
            product.departamento = departamento
        if numero_celular:
            product.numero_celular = numero_celular

        # Manejo de la imagen
        if imagen_file:
            if not imagen_file.content_type.startswith('image/'):
                return jsonify({"error": "El archivo no es una imagen válida"}), 400

            # Guardar el archivo usando el nombre original
            filename = imagen_file.filename
            imagen_path = os.path.join(upload_folder, filename)
            imagen_file.save(imagen_path)
            product.imagen_url = f'/uploads/{filename}'  # Actualiza la URL de la imagen

        db.session.commit()
        print("Product updated successfully.")

        return jsonify({"mensaje": "Producto actualizado exitosamente"}), 200

    except Exception as e:
        print(f"Error updating product: {str(e)}")  # Imprimir el error para depuración
        return jsonify({"error": str(e)}), 500

        # Ruta para eliminar un producto por ID
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def eliminar_producto(product_id):
    try:
        product = Product.query.get(product_id)
        if product is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({"mensaje": "Producto eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500