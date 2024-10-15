from flask import Flask, send_from_directory
from database import db
from models import Product, Categoria
from routes.products import product_bp 
from flask_cors import CORS

# Inicializa la aplicación de Flask
app = Flask(__name__)

# Configura la URI de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2021@localhost:3307/sobramat_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa SQLAlchemy
db.init_app(app)

# Registra el Blueprint
app.register_blueprint(product_bp, url_prefix='/products')

# Habilita CORS
CORS(app, origins=["http://localhost:5173"])

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(debug=True)