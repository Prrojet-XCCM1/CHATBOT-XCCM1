from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_pyfile('config.py')


    # Configuration basique
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
    
    # CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Setup Swagger
    from app.api.swagger import setup_swagger
    setup_swagger(app)
    
    return app