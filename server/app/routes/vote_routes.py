from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Vote, Post, User

vote_bp = Blueprint('vote_bp', __name__)

@vote_bp.route('/posts/<int:post_id>/vote', methods=['POST'])
@jwt_required()
def vote_post(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    is_upvote = data.get('is_upvote')

    if is_upvote is None:
        return jsonify({'error': 'is_upvote is required'}), 400

    post = Post.query.get(post_id)
    if not post or post.is_deleted:
        return jsonify({'error': 'Post not found'}), 404

    existing_vote = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()

    if existing_vote:
        if existing_vote.is_upvote == is_upvote:
            db.session.delete(existing_vote)  # Remove vote if user clicks the same vote again
            db.session.commit()
            return jsonify({'message': 'Vote removed'})
        else:
            existing_vote.is_upvote = is_upvote  # Update vote type
    else:
        new_vote = Vote(user_id=user_id, post_id=post_id, is_upvote=is_upvote)
        db.session.add(new_vote)
    
    db.session.commit()
    return jsonify({'message': 'Vote registered'})

@vote_bp.route('/posts/<int:post_id>/votes', methods=['GET'])
def get_vote_counts(post_id):
    post = Post.query.get(post_id)
    if not post or post.is_deleted:
        return jsonify({'error': 'Post not found'}), 404
    
    upvotes = Vote.query.filter_by(post_id=post_id, is_upvote=True).count()
    downvotes = Vote.query.filter_by(post_id=post_id, is_upvote=False).count()
    
    return jsonify({'post_id': post_id, 'upvotes': upvotes, 'downvotes': downvotes})
