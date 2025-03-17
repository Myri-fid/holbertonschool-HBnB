from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('admin', description='Admin operations')

def is_admin():
    """Helper function to check if the current user is an admin"""
    current_user = get_jwt_identity()
    if not current_user.get('is_admin'):
        return False
    return True

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        """Create a new user (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        password = data.get('password')

        if facade.get_user_by_email(email):
            return {'error': 'Email is already in use'}, 400

        if len(password) < 6:
            return {'error': 'Password must be at least 6 characters long'}, 400

        data['password'] = facade.hash_password(password)  # Ensure password is hashed

        try:
            new_user = facade.create_user(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'User created successfully', 'id': new_user.id}, 201


@api.route('/users/<int:user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        """Modify a user's details (Admin only, including email and password)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        password = data.get('password')

        if email and facade.get_user_by_email(email):
            return {'error': 'Email is already in use'}, 400

        if password:
            if len(password) < 6:
                return {'error': 'Password must be at least 6 characters long'}, 400
            data['password'] = facade.hash_password(password)  # Hash new password

        try:
            updated_user = facade.update_user(user_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'User updated successfully', 'id': updated_user.id}, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        """Add a new amenity (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        try:
            new_amenity = facade.create_amenity(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Amenity added successfully', 'id': new_amenity.id}, 201


@api.route('/amenities/<int:amenity_id>')
class AdminAmenityUpdate(Resource):
    @jwt_required()
    def put(self, amenity_id):
        """Modify an amenity's details (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Amenity updated successfully', 'id': updated_amenity.id}, 200



@api.route('/places/<int:place_id>')
class AdminPlaceUpdateDelete(Resource):
    @jwt_required()
    def put(self, place_id):
        """Modify any place (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        try:
            updated_place = facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Place updated successfully', 'id': updated_place.id}, 200

    @jwt_required()
    def delete(self, place_id):
        """Delete any place (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        deleted = facade.delete_place(place_id)
        if not deleted:
            return {'error': 'Place not found'}, 404

        return {'message': 'Place deleted successfully'}, 204


@api.route('/reviews/<int:review_id>')
class AdminReviewUpdateDelete(Resource):
    @jwt_required()
    def put(self, review_id):
        """Modify any review (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        try:
            updated_review = facade.update_review(review_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Review updated successfully', 'id': updated_review.id}, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete any review (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review deleted successfully'}, 204
