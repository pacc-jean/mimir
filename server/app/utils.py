from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()  # Get the logged-in user's ID
        user = User.query.get(user_id)  # Fetch user from DB

        if not user or not user.is_admin:  # Check if user exists and is an admin
            return jsonify({'error': 'Admin access required'}), 403

        return f(*args, **kwargs)

    return decorated_function
