from flask_restx import Namespace, Resource, fields
from app.services import facade
from app import bcrypt
import re

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Validate input fields
        if not isinstance(user_data['first_name'], str) or not user_data['first_name'].strip():
            api.abort(400, "First name must be a non-empty string")

        if not isinstance(user_data['last_name'], str) or not user_data['last_name'].strip():
            api.abort(400, "Last name must be a non-empty string")

        email_pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z-_]+\.[a-zA-Z]{2,}$"
        if not isinstance(user_data['email'], str) or not re.match(email_pattern, user_data['email']):
            api.abort(400, "Invalid email format")

        if facade.get_user_by_email(user_data['email']):
            api.abort(400, "Email already registered")

        # Validate and hash password
        if 'password' not in user_data or not isinstance(user_data['password'], str) or len(user_data['password']) < 6:
            api.abort(400, "Password must be at least 6 characters long")

        user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email
        }, 201

    @api.response(200, "Successfully retrieved user list")
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return [{"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email} for user in users], 200


@api.route('/<int:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user"""
        user_data = api.payload
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        if "email" in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user.id:
                api.abort(400, "Email already registered by another user")

        if "password" in user_data:
            if len(user_data['password']) < 6:
                api.abort(400, "Password must be at least 6 characters long")
            user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

        try:
            updated_user = facade.update_user(user_id, user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, f"Error: {str(e)}")

        return {
            "id": updated_user.id,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "email": updated_user.email
        }, 200

    @api.response(204, 'User successfully deleted')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return '', 204
