import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from models import Product,Categoria
from extensions import db

product_bp = Blueprint('products', __name__)

def upload_image_and_get_url(imagen_file):
    # Crear un nombre de archivo único
    image_filename = f"{uuid.uuid4()}.jpg"
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
    
    # Guardar la imagen
    imagen_file.save(upload_path)
    
    # Retornar la URL de la imagen
    return f"http://localhost:5000/uploads/{image_filename}"

@product_bp.route('/agregar-producto', methods=['POST'])
def agregar_producto():
    try:
        data = request.form.to_dict()
        
        # Obtener la imagen de los archivos subidos
        imagen_file = request.files.get('imagen_url')

        # Procesar la imagen si se envía
        if imagen_file:
            imagen_url = upload_image_and_get_url(imagen_file)
        else:
            return jsonify({"error": "Se requiere una imagen"}), 400

        # Resto de los datos
        nuevo_producto = Product(
            nombre_producto=data['nombre_producto'],
            estado_producto=data['estado_producto'],
            precio=float(data['precio']),
            descripcion=data['descripcion'],
            categoria_id=int(data['categoria_id']),
            departamento=data['departamento'],
            numero_celular=data['numero_celular'],
            imagen_url=imagen_url,
            usuario_id=int(data['usuario_id'])
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        return jsonify({"mensaje": "Producto agregado exitosamente", "producto": nuevo_producto.to_dict()}), 201

    except Exception as e:
        return jsonify({"error": "Ocurrió un error al agregar el producto", "detalles": str(e)}), 500

@product_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def get_products_by_user(usuario_id):
    try:
        products = Product.query.filter_by(usuario_id=usuario_id).all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(product.to_dict()), 200

@product_bp.route('/<int:product_id>', methods=['PUT'])
def actualizar_producto(product_id):
    try:
        product = Product.query.get(product_id)
        if product is None:
            return jsonify({"error": "Producto no encontrado"}), 404

        data = request.form.to_dict()
        imagen_file = request.files.get('imagen_url')

        if imagen_file:
            imagen_url = upload_image_and_get_url(imagen_file)
            product.imagen_url = imagen_url  # Actualiza la imagen

        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()
        return jsonify({"mensaje": "Producto actualizado exitosamente", "producto": product.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
@product_bp.route('/all', methods=['GET'])
def get_all_products():
    estado = request.args.get('estado')
    categoria = request.args.get('categoria')
    precio_max = request.args.get('precio')
    departamento = request.args.get('departamento')

    query = Product.query

    if estado:
        query = query.filter(Product.estado_producto == estado)  # Verifica que el atributo sea `estado_producto`
    if categoria:
        query = query.filter(Product.categoria_id == categoria)  # Asegúrate de que esto sea correcto
    if precio_max:
        query = query.filter(Product.precio <= float(precio_max))
    if departamento:
        query = query.filter(Product.departamento == departamento)

    productos = query.all()
    
    return jsonify([producto.to_dict() for producto in productos]), 200
@product_bp.route('/categories/all', methods=['GET'])
def get_categories():
    connection = get_db_connection()  # Conéctate a tu base de datos
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM categorias")  # Cambia esto según tu estructura de base de datos
        categories = cursor.fetchall()
        result = [{"id": cat[0], "nombre": cat[1]} for cat in categories]  # Ajusta según el esquema de tu tabla
        return jsonify(result), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error al obtener categorías"}), 500