from flask import Blueprint, request, jsonify
from extensions import db  # Cambia esta línea si es necesario
from models import Usuarios
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    correo_electronico = data.get('correo_electronico')
    contrasena = data.get('contrasena')

    if not all([nombre_usuario, correo_electronico, contrasena]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    hashed_password = generate_password_hash(contrasena)
    nuevo_usuario = Usuarios(
        nombre_usuario=nombre_usuario,
        correo_electronico=correo_electronico,
        contrasena=hashed_password
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo_electronico = data.get('correo_electronico')
    contrasena = data.get('contrasena')

    # Busca por correo_electronico
    user = Usuarios.query.filter_by(correo_electronico=correo_electronico).first()

    if user and check_password_hash(user.contrasena, contrasena):
        return jsonify({"mensaje": "Inicio de sesión exitoso", "user": user.to_dict()}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401
