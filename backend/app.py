import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.auth import auth_bp
from routes.products import product_bp
from extensions import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2021@localhost:3307/sobramat_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'  # Asegúrate de que esta carpeta exista

    db.init_app(app)

    # Configuración de CORS: permite todos los orígenes y métodos para pruebas
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/products')

    return app

# Definimos la app antes de usarla en esta ruta
app = create_app()

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
