from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Post, Vote, Community, User

post_bp = Blueprint('post', __name__, url_prefix='/posts')

# Create a post
@post_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()

    community = Community.query.get(data.get('community_id'))
    if not community or community.is_deleted:
        return jsonify({'message': 'Community not found'}), 404
    
    post = Post(title=data['title'], content=data['content'], user_id=user_id, community_id=data['community_id'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully', 'post_id': post.id}), 201

# Get posts with filtering options
@post_bp.route('', methods=['GET'])
def get_posts():
    sort_by = request.args.get('sort_by', 'recent')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Post.query.filter_by(is_deleted=False)
    
    if sort_by == 'oldest':
        query = query.order_by(Post.created_at.asc())
    elif sort_by == 'popularity':
        query = query.outerjoin(Vote).group_by(Post.id).order_by(db.func.count(Vote.id).desc())
    else:  # Default is 'recent'
        query = query.order_by(Post.created_at.desc())
    
    posts = query.paginate(page=page, per_page=per_page, error_out=False)
    
    result = []
    for post in posts.items:
        author = User.query.get(post.user_id)
        vote_count = Vote.query.filter_by(post_id=post.id).count()
        result.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'author': author.username,
            'community_id': post.community_id,
            'vote_count': vote_count
        })
    
    return jsonify({'posts': result, 'total_pages': posts.pages, 'current_page': page})

# Update a post
@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.get_json()
    user_id = int(get_jwt_identity())
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})

# Delete a post (soft delete)
@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = int(get_jwt_identity())
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    post.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})
