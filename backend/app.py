from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.products import product_bp
from extensions import db  # Importa db desde extensions

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2021@localhost:3307/sobramat_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app, origins=["http://localhost:5173"])

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/products')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
