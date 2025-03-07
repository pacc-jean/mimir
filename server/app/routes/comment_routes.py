from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Comment, User, Post

comment_bp = Blueprint('comment', __name__, url_prefix='/comments')

# Create a comment
@comment_bp.route('/post/<int:post_id>', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment added successfully', 'comment': {
        'id': comment.id,
        'content': comment.content,
        'author': User.query.get(user_id).username,
        'created_at': comment.created_at
    }}), 201

# Update a comment
@comment_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    data = request.get_json()
    user_id = int(get_jwt_identity())
    comment = Comment.query.get(comment_id)

    if not comment or comment.is_deleted:
        return jsonify({'error': 'Comment not found'}), 404

    if comment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    comment.content = data.get('content', comment.content)
    db.session.commit()
    
    return jsonify({'message': 'Comment updated successfully', 'comment': {
        'id': comment.id,
        'content': comment.content,
        'updated_at': comment.updated_at
    }}), 200

# Delete a comment (soft delete)
@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = int(get_jwt_identity())
    comment = Comment.query.get(comment_id)

    if not comment or comment.is_deleted:
        return jsonify({'error': 'Comment not found'}), 404

    if comment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    comment.is_deleted = True
    db.session.commit()
    
    return jsonify({'message': 'Comment deleted successfully'}), 200

# Get comments for a post
@comment_bp.route('/post/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    comments = Comment.query.filter_by(post_id=post_id, is_deleted=False).all()
    return jsonify({'comments': [
        {
            'id': c.id,
            'content': c.content,
            'author': User.query.get(c.user_id).username,
            'created_at': c.created_at
        } for c in comments
    ]}), 200
