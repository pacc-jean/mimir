from flask import Blueprint


from .auth_routes import auth_bp
from .community_routes import community_bp
from .post_routes import post_bp
from .comment_routes import comment_bp
from .vote_routes import vote_bp
from .category_routes import category_bp


blueprints = [auth_bp, community_bp, post_bp, comment_bp, vote_bp, category_bp]

def register_routes(app):
    for bp in blueprints:
        app.register_blueprint(bp)
