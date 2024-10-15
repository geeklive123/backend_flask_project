from database import db  # Importa db desde el nuevo archivo

class Product(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(255), nullable=False)
    estado_producto = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    departamento = db.Column(db.String(255), nullable=False)
    numero_celular = db.Column(db.String(15))
    imagen_url = db.Column(db.String(255))

    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_producto": self.nombre_producto,
            "estado_producto": self.estado_producto,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "categoria_id": self.categoria_id,
            "departamento": self.departamento,
            "numero_celular": self.numero_celular,
            "imagen_url": self.imagen_url,
            "categoria": self.categoria.nombre if self.categoria else None
        }

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    