import os
from flask import Blueprint, request, jsonify
from models import Product, Categoria, Usuarios  # Importa los modelos
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
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        print(f"Error al obtener productos: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Ruta para obtener un producto por ID
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(product.to_dict()), 200

# Función para manejar la creación o actualización de productos
def process_product_data(request, product=None, usuario_id=None):
    nombre = request.form.get('nombre_producto')
    estado = request.form.get('estado_producto')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    categoria_id = request.form.get('categoria_id')
    departamento = request.form.get('departamento')
    numero_celular = request.form.get('numero_celular')
    imagen_file = request.files.get('imagen_url')

    if not all([nombre, estado, descripcion, precio, categoria_id, departamento, numero_celular, imagen_file]) and product is None:
        return jsonify({"error": "Faltan datos"}), 400

    if precio:
        try:
            precio = float(precio)
        except ValueError:
            return jsonify({"error": "Precio inválido"}), 400

    # Guarda la imagen si existe
    if imagen_file and imagen_file.content_type.startswith('image/'):
        filename = imagen_file.filename
        imagen_path = os.path.join(upload_folder, filename)
        imagen_file.save(imagen_path)
        imagen_url = f'/uploads/{filename}'
    elif product:
        imagen_url = product.imagen_url
    else:
        return jsonify({"error": "Imagen no proporcionada o inválida"}), 400

    return {
        "nombre_producto": nombre,
        "estado_producto": estado,
        "descripcion": descripcion,
        "precio": precio,
        "categoria_id": int(categoria_id),
        "departamento": departamento,
        "numero_celular": numero_celular,
        "imagen_url": imagen_url,
        "usuario_id": usuario_id  # Agrega el usuario_id aquí
    }

# Ruta para agregar un nuevo producto
@product_bp.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    try:
        usuario_id = request.form.get('usuario_id')  # Obtén el usuario_id del formulario o de otra fuente
        product_data = process_product_data(request, usuario_id=usuario_id)

        if isinstance(product_data, dict) and "error" in product_data:
            return jsonify(product_data), 400

        nuevo_producto = Product(**product_data)

        db.session.add(nuevo_producto)
        db.session.commit()

        return jsonify({"mensaje": "Producto agregado exitosamente", "producto": nuevo_producto.to_dict()}), 201

    except Exception as e:
        print(f"Error en agregar_producto: {str(e)}")
        return jsonify({"error": "Ocurrió un error al agregar el producto", "detalles": str(e)}), 500

        
# Ruta para actualizar un producto por ID
@product_bp.route('/<int:product_id>', methods=['PUT'])
def actualizar_producto(product_id):
    try:
        usuario_id = request.form.get('usuario_id')  # Obtén el usuario_id del formulario o de otra fuente

        product = Product.query.get(product_id)
        if product is None or product.usuario_id != usuario_id:
            return jsonify({"error": "Producto no encontrado o no autorizado"}), 404

        product_data = process_product_data(request, product, usuario_id=usuario_id)
        if isinstance(product_data, dict) and "error" in product_data:
            return jsonify(product_data), 400

        for key, value in product_data.items():
            setattr(product, key, value)

        db.session.commit()
        return jsonify({"mensaje": "Producto actualizado exitosamente"}), 200

    except Exception as e:
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
