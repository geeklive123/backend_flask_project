from flask import Flask
from models import db  # Importa el db desde models
from routes.products import product_bp  # Importa el blueprint
from config import Config  # Importa la configuración

app = Flask(__name__)

# Carga la configuración de la clase Config desde config.py
app.config.from_object(Config)

# Inicializa la base de datos con la app
db.init_app(app)

# Registra el blueprint para las rutas
app.register_blueprint(product_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas basadas en los modelos definidos
    app.run(debug=True)
