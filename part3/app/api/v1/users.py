from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
import re

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data or email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not isinstance(user_data.get(field, ''), str) or not user_data[field].strip():
                api.abort(400, f"{field} must be a non-empty string")

        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, user_data['email']):
            api.abort(400, "Invalid email format")

        if facade.get_user_by_email(user_data['email']):
            api.abort(400, "Email already registered")

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return new_user.display(), 201

    @api.response(200, "Successfully retrieved users list")
    def get(self):
        """Retrieve all users"""
        return facade.get_all_users()

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.display(), 200

    @jwt_required()
    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(403, 'Unauthorized')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or email already registered')
    def put(self, user_id):
        """Update user - Only the owner can modify their data (except email/password)"""
        user_data = api.payload
        current_user_id = get_jwt_identity()

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if str(user.id) != str(current_user_id):
            return {'error': 'Unauthorized'}, 403

        if 'email' in user_data or 'password' in user_data:
            return {'error': 'Email and password cannot be updated'}, 400

        try:
            user.update(user_data)
            updated_user = facade.update_user(user_id, user.display())
        except (ValueError, TypeError) as e:
            api.abort(400, f"Error: {str(e)}")

        return updated_user.display(), 200

    @jwt_required()
    @api.response(204, 'User successfully deleted')
    @api.response(403, 'Unauthorized')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete user - Only the owner can delete their account"""
        current_user_id = get_jwt_identity()

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if str(user.id) != str(current_user_id):
            return {'error': 'Unauthorized'}, 403

        facade.delete_user(user_id)
        return '', 204
