import re
from app.services import facade
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    def post(self):
        """Register a new place (Only authenticated users)"""
        place_data = api.payload
        owner_id = get_jwt_identity()
        place_data['owner_id'] = owner_id

        if not isinstance(place_data.get('title'), str) or not place_data['title'].strip():
            return {'error': 'Title must be a non-empty string'}, 400

        if not isinstance(place_data.get('price'), (float, int)) or place_data['price'] <= 0:
            return {'error': 'Price must be a positive number'}, 400

        if not isinstance(place_data.get('latitude'), (float, int)) or not (-90.0 <= place_data['latitude'] <= 90.0):
            return {'error': 'Invalid latitude value'}, 400

        if not isinstance(place_data.get('longitude'), (float, int)) or not (-180.0 <= place_data['longitude'] <= 180.0):
            return {'error': 'Invalid longitude value'}, 400

        try:
            place = facade.create_place(place_data)
            return jsonify(place.to_dict()), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return jsonify([place.to_dict() for place in places]), 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place_by_id(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        return jsonify(place.to_dict()), 200

    @jwt_required()
    @api.expect(place_model)
    def put(self, place_id):
        """Update a place's information - Only the owner can modify"""
        user_id = get_jwt_identity()
        place_data = api.payload

        place = facade.get_place_by_id(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if str(place.owner_id) != str(user_id):
            return {'error': 'Unauthorized action'}, 403

        if 'title' in place_data and (not isinstance(place_data['title'], str) or not place_data['title'].strip()):
            return {'error': 'Title must be a non-empty string'}, 400

        if 'price' in place_data and (not isinstance(place_data['price'], (float, int)) or place_data['price'] <= 0):
            return {'error': 'Price must be a positive number'}, 400

        try:
            updated_place = facade.update_place(place_id, place_data)
            return jsonify(updated_place.to_dict()), 200
        except ValueError as e:
            return {'error': str(e)}, 400
