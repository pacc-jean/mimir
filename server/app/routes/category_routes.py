from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Category, Community, User
from app.utils import admin_required  # Ensure only admin can create/update/delete categories
from datetime import datetime

category_bp = Blueprint('category_bp', __name__)

# Create a new category (Admin only)
@category_bp.route('/categories', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Category name is required'}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Category already exists'}), 400

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully', 'category': {'id': category.id, 'name': category.name}}), 201

# Update a category (Admin only)
@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)

    data = request.get_json()
    new_name = data.get('name')

    if new_name:
        if Category.query.filter(Category.id != category_id, Category.name == new_name).first():
            return jsonify({'error': 'Category name already exists'}), 400
        category.name = new_name
        category.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Category updated successfully', 'category': {'id': category.id, 'name': category.name}})

# Soft delete a category (Admin only)
@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    category.is_deleted = True
    category.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})

# Get all categories (Users can access)
@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.filter_by(is_deleted=False).all()
    
    return jsonify([
        {'id': cat.id, 'name': cat.name}
        for cat in categories
    ])

# Get a single category with its communities (Users can access)
@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.filter_by(id=category_id, is_deleted=False).first()

    if not category:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({
        'id': category.id,
        'name': category.name,
        'communities': [
            {'id': comm.id, 'name': comm.name, 'description': comm.description, 'members_count': comm.members_count}
            for comm in category.communities if not comm.is_deleted
        ]
    })
