from extensions import db

class Product(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(255), nullable=False)
    estado_producto = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)
    departamento = db.Column(db.String(255), nullable=False)
    numero_celular = db.Column(db.String(15), nullable=True)
    imagen_url = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    def __init__(self, nombre_producto, estado_producto, precio, descripcion, categoria_id, departamento, numero_celular, imagen_url, usuario_id):
        self.nombre_producto = nombre_producto
        self.estado_producto = estado_producto
        self.precio = precio
        self.descripcion = descripcion
        self.categoria_id = categoria_id
        self.departamento = departamento
        self.numero_celular = numero_celular
        self.imagen_url = imagen_url
        self.usuario_id = usuario_id

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_producto": self.nombre_producto,
            "estado_producto": self.estado_producto,
            "precio": self.precio,
            "descripcion": self.descripcion,
            "categoria_id": self.categoria_id,
            "departamento": self.departamento,
            "numero_celular": self.numero_celular,
            "imagen_url": self.imagen_url,
            "usuario_id": self.usuario_id
        }


class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    productos = db.relationship('Product', backref='categoria', lazy=True)

    def __init__(self, nombre, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre_usuario, correo_electronico, contrasena):
        self.nombre_usuario = nombre_usuario
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "correo_electronico": self.correo_electronico
        }
