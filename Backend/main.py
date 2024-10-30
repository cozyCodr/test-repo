from flask import Flask, redirect
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import DevConfig
from models import db
from datetime import timedelta

# Import routes
from auth import auth_blueprint
from key_concepts import concepts_blueprint
from dashboard import dashboard_blueprint


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*",
         "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"]}})

    Migrate(app, db)

    # Configure JWT
    app.config['JWT_SECRET_KEY'] = 'aee8207fef0e873016e85d6e'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # Initialize API with swagger documentation
    api = Api(
        app,
        version='1.0',
        title='Learning Platform API',
        description='A REST API for managing educational content and key concepts',
        doc='/api/docs'
    )

    # Register namespaces
    api.add_namespace(auth_blueprint, path='/api/auth')
    api.add_namespace(concepts_blueprint, path='/api/concepts')
    api.add_namespace(dashboard_blueprint, path='/api/dashboard')
    api.add_namespace(dashboard_blueprint, path='/api/uploads')

    # Add the Home resource

    @api.route('/home')
    class Home(Resource):
        def get(self):
            return {'message': 'Welcome to the Auth API'}

    @api.route('/hello')
    class HelloWorld(Resource):
        def get(self):
            return {'hello': 'world'}

    @api.route('/')
    class RootResource(Resource):
        def get(self):
            return {'message': 'Welcome to the Learning Platform API'}

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'message': 'Internal server error'}, 500

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has expired'}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'message': 'Invalid token'}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'message': 'Missing authorization token'}, 401

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
