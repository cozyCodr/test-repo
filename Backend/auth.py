# auth/routes.py
from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from models import *

auth_blueprint = Namespace('auth', description='Authentication operations')

# Improved models with validation
signup_model = auth_blueprint.model("SignUp", {
    "username": fields.String(required=True, min_length=3, max_length=50),
    "email": fields.String(required=True),
    "university": fields.String(required=True),
    "school": fields.String(required=True),
    "password": fields.String(required=True, min_length=8),
    "confirmPassword": fields.String(required=True)
})

login_model = auth_blueprint.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

# Response models
auth_response = auth_blueprint.model("AuthResponse", {
    "access_token": fields.String(),
    "refresh_token": fields.String(),
    "user": fields.Nested({
        "id": fields.Integer(),
        "username": fields.String(),
        "email": fields.String(),
        "university": fields.String(),
        "school": fields.String()
    })
})


@auth_blueprint.route('/signup')
class SignUp(Resource):
    @auth_blueprint.expect(signup_model)
    @auth_blueprint.response(201, 'Success', auth_response)
    @auth_blueprint.response(400, 'Validation Error')
    def post(self):
        """Register a new student"""
        data = request.get_json()

        # Validation
        if data['password'] != data['confirmPassword']:
            return {'message': 'Passwords do not match'}, 400

        if Student.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400

        try:
            new_student = Student(
                username=data['username'],
                email=data['email'].lower(),
                university=data['university'],
                school=data['school'],
                password=generate_password_hash(data['password']),
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow()
            )

            new_student.save()

            # Generate tokens
            access_token = create_access_token(identity=new_student.id)
            refresh_token = create_refresh_token(identity=new_student.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': new_student.id,
                    'username': new_student.username,
                    'email': new_student.email,
                    'university': new_student.university,
                    'school': new_student.school
                }
            }, 201

        except Exception as e:
            return {'message': str(e)}, 400


@auth_blueprint.route('/login')
class Login(Resource):
    @auth_blueprint.expect(login_model)
    @auth_blueprint.response(200, 'Success', auth_response)
    @auth_blueprint.response(401, 'Authentication Failed')
    def post(self):
        """Authenticate a student"""
        data = request.get_json()

        student = Student.query.filter_by(email=data['email'].lower()).first()

        if not student or not check_password_hash(student.password, data['password']):
            return {'message': 'Invalid email or password'}, 401

        # Update last login
        student.last_login = datetime.utcnow()
        student.save()

        access_token = create_access_token(identity=student.id)
        refresh_token = create_refresh_token(identity=student.id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': student.id,
                'username': student.username,
                'email': student.email,
                'university': student.university,
                'school': student.school
            }
        }


@auth_blueprint.route('/refresh')
class RefreshToken(Resource):
    @jwt_required(optional=True)  # Optional Jwt(refresh=True)
    def post(self):
        """Refresh access token"""
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {'access_token': new_access_token}


@auth_blueprint.route('/me')
class UserProfile(Resource):
    @jwt_required(optional=True)  # Optional Jwt()
    def get(self):
        """Get current user profile"""
        current_user_id = get_jwt_identity()
        student = Student.query.get(current_user_id)

        return {
            'id': student.id,
            'username': student.username,
            'email': student.email,
            'university': student.university,
            'school': student.school,
            'created_at': student.created_at.isoformat(),
            'last_login': student.last_login.isoformat()
        }
