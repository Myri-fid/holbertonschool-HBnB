from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from flask_jwt_extended import JWTManager
from app.api.v1.users import api as users_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

# Initialisation de JWT
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    # Créer une instance de l'application Flask
    app = Flask(__name__)
    app.config.from_object(config_class)  # Charger la configuration
 
    # Initialiser JWTManager et Flask-Bcrypt
    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)

    # Initialiser l'API Flask-RESTx
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Ajouter les namespaces (endpoints de l'API)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app
