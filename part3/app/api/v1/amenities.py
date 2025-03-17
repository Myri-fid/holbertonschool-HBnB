from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = request.get_json()
        
        if not isinstance(data.get('name'), str) or not data['name'].strip():
            api.abort(400, "Amenity name must be a non-empty string")

        existing_amenity = facade.get_amenity_by_name(data['name'])
        if existing_amenity:
            api.abort(400, "Amenity already exists")

        amenity = facade.create_amenity(data['name'])
        return jsonify({'id': amenity.id, 'name': amenity.name}), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return jsonify([{'id': amenity.id, 'name': amenity.name} for amenity in amenities]), 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity_by_id(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return jsonify({'id': amenity.id, 'name': amenity.name}), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid data')
    def put(self, amenity_id):
        """Update amenity information"""
        data = request.get_json()


        if not isinstance(data.get('name'), str) or not data['name'].strip():
            api.abort(400, "Amenity name must be a non-empty string")

        amenity = facade.get_amenity_by_id(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")

        existing_amenity = facade.get_amenity_by_name(data['name'])
        if existing_amenity and existing_amenity.id != amenity_id:
            api.abort(400, "Amenity with this name already exists")

        amenity.name = data['name']
        updated_amenity = facade.update_amenity(amenity_id, {'name': data['name']})
        return jsonify({'id': updated_amenity.id, 'name': updated_amenity.name}), 200
