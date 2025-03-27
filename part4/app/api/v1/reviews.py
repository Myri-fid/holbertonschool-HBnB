import re
import uuid
from app.services import facade
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

def is_valid_uuid(value):
    """Check if a given value is a valid UUID."""
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    def post(self):
        """Create a new review (Users can only review places they do not own)"""
        review_data = api.payload

        # Validate review text
        if not isinstance(review_data.get('text'), str) or not review_data['text'].strip():
            return {'error': 'Review text must be a non-empty string'}, 400

        # Validate rating
        rating = review_data.get('rating')
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {'error': 'Invalid rating. Choose between 1 and 5'}, 400

        # Validate place ID
        place_id = review_data.get('place_id')
        if not is_valid_uuid(place_id):
            return {'error': 'Invalid place ID format'}, 400

        # Prevent reviewing own place
        user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 400
        if str(place.owner_id) == str(user_id):
            return {'error': 'You cannot review your own place'}, 403

        # Ensure unique review per user per place
        if facade.get_review_by_user_and_place(user_id, place_id):
            return {'error': 'You have already reviewed this place'}, 403

        review_data['user_id'] = user_id

        try:
            review = facade.create_review(review_data)
        except (ValueError, TypeError) as error:
            return {'error': str(error)}, 400

        return jsonify(review.to_dict()), 201

    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return jsonify([review.to_dict() for review in reviews]), 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return jsonify(review.to_dict()), 200

    @jwt_required()
    @api.expect(review_model)
    def put(self, review_id):
        """Update a review - Users can only modify reviews they created"""
        user_id = get_jwt_identity()
        data = request.get_json()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if str(review.user_id) != str(user_id):
            return {'error': 'Unauthorized action'}, 403

        # Validate updated text
        if 'text' in data and (not isinstance(data['text'], str) or not data['text'].strip()):
            return {'error': 'Review text must be a non-empty string'}, 400

        # Validate updated rating
        if 'rating' in data and (not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5)):
            return {'error': 'Invalid rating. Choose between 1 and 5'}, 400

        try:
            updated_review = facade.update_review(review_id, data)
        except (ValueError, TypeError) as error:
            return {'error': str(error)}, 400

        return jsonify(updated_review.to_dict()), 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review - Users can only delete reviews they created"""
        user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if str(review.user_id) != str(user_id):
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return '', 204


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'Place not found or no reviews for this place'}, 404
        return jsonify(reviews), 200
