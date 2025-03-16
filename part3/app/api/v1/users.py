from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or restricted update fields')
    def put(self, user_id):
        """Update user - Only the owner can modify their data (except email/password)"""
        user_data = api.payload
        current_user_id = get_jwt_identity()

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if str(user.id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400

        try:
            user.update(user_data)
            updated_user = facade.update_user(user_id, user.display())
        except (ValueError, TypeError) as e:
            api.abort(400, f"Error: {str(e)}")

        return updated_user.display(), 200

    @jwt_required()
    @api.response(204, 'User successfully deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete user - Only the owner can delete their account"""
        current_user_id = get_jwt_identity()

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if str(user.id) != str(current_user_id):
            return {'error': 'Unauthorized action'}, 403

        facade.delete_user(user_id)
        return '', 204
