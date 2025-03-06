from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Community, User

community_bp = Blueprint('community', __name__, url_prefix='/communities')

# Create a community
@community_bp.route('', methods=['POST'])
@jwt_required()
def create_community():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    category_id = data.get('category_id')
    user_id = get_jwt_identity()

    if not name or not category_id:
        return jsonify({'error': 'Name and category are required'}), 400

    existing_community = Community.query.filter_by(name=name).first()
    if existing_community:
        return jsonify({'error': 'Community with this name already exists'}), 400

    community = Community(name=name, description=description, category_id=category_id, creator_id=user_id)
    db.session.add(community)
    db.session.commit()

    return jsonify({'message': 'Community created successfully', 'community': {'id': community.id, 'name': community.name}}), 201

# Update a community
@community_bp.route('/<int:community_id>', methods=['PUT'])
@jwt_required()
def update_community(community_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    community = Community.query.get_or_404(community_id)
    if community.is_deleted:
        return jsonify({'error': 'Community not found'}), 404
    
    if community.creator_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    community.name = data.get('name', community.name)
    community.description = data.get('description', community.description)
    db.session.commit()

    return jsonify({'message': 'Community updated successfully'})

# Soft delete a community
@community_bp.route('/<int:community_id>', methods=['DELETE'])
@jwt_required()
def delete_community(community_id):
    user_id = get_jwt_identity()
    community = Community.query.get_or_404(community_id)

    if community.is_deleted:
        return jsonify({'error': 'Community not found'}), 404

    if community.creator_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    community.is_deleted = True
    db.session.commit()

    return jsonify({'message': 'Community deleted successfully'})

# Get all communities (excluding deleted ones)
@community_bp.route('', methods=['GET'])
def get_communities():
    communities = Community.query.filter_by(is_deleted=False).all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in communities])

# Get a single community
@community_bp.route('/<int:community_id>', methods=['GET'])
def get_community(community_id):
    community = Community.query.get_or_404(community_id)
    if community.is_deleted:
        return jsonify({'error': 'Community not found'}), 404

    return jsonify({'id': community.id, 'name': community.name, 'description': community.description})

# Join a community
@community_bp.route('/<int:community_id>/join', methods=['POST'])
@jwt_required()
def join_community(community_id):
    user_id = get_jwt_identity()
    community = Community.query.get_or_404(community_id)
    user = User.query.get(user_id)

    if community.is_deleted:
        return jsonify({'error': 'Community not found'}), 404

    if user in community.members:
        return jsonify({'error': 'You are already a member of this community'}), 400

    community.members.append(user)
    db.session.commit()

    return jsonify({'message': 'Joined community successfully'})

# Leave a community
@community_bp.route('/<int:community_id>/leave', methods=['POST'])
@jwt_required()
def leave_community(community_id):
    user_id = get_jwt_identity()
    community = Community.query.get_or_404(community_id)
    user = User.query.get(user_id)

    if community.is_deleted:
        return jsonify({'error': 'Community not found'}), 404

    if user not in community.members:
        return jsonify({'error': 'You are not a member of this community'}), 400

    community.members.remove(user)
    db.session.commit()

    return jsonify({'message': 'Left community successfully'})
