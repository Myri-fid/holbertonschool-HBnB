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

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Create a new review (Users can only review places they do not own)"""
        review_data = api.payload
        if not review_data:
            return {'error': 'Invalid input data'}, 400

        user_id = get_jwt_identity()
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')

        # Validate Place Existence
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 400

        # Prevent User from Reviewing Own Place
        if str(place.owner_id) == str(user_id):
            return {'error': 'You cannot review your own place'}, 403

        # Validate Unique Review per Place
        existing_review = facade.get_review_by_user_and_place(user_id, place_id)
        if existing_review:
            return {'error': 'You have already reviewed this place'}, 403

        # Validate Rating Range
        if not (1 <= rating <= 5):
            return {'error': 'Invalid rating. Choose between 1 and 5'}, 400

        review_data['user_id'] = user_id  # Assign current user ID to the review

        try:
            review = facade.create_review(review_data)
        except (ValueError, TypeError) as error:
            return {'error': str(error)}, 400

        return jsonify(review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return jsonify(reviews), 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return jsonify(review), 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review - Users can only modify reviews they created"""
        user_id = get_jwt_identity()
        data = request.get_json()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if str(review.user_id) != str(user_id):
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_review = facade.update_review(review_id, data)
        except (ValueError, TypeError) as error:
            return {'error': str(error)}, 400

        return jsonify(updated_review), 200

    @jwt_required()
    @api.response(204, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
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
