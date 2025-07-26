import re
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Users
from config import Config
import uuid

users_bp = Blueprint('Users', __name__)

error_pwd_validation_msg = 'Password must contain at least 6 characters, including Upper/Lowercase, special characters and numbers'


# Fetch user profile
@users_bp.route(Config.USER_PROFILE, methods=['GET'])
@jwt_required()
def user_profile(user_id):
    if get_jwt_identity() == user_id:
        user = Users.query.get(user_id)
        if not user:
            abort(404)
        return jsonify({
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        })
    abort(401)


# Update profile
@users_bp.route(Config.UPDATE_PROFILE, methods=['PUT'])
@jwt_required()
def update_profile(user_id):
    if get_jwt_identity() == user_id:
        user = Users.query.get(user_id)
        if not user:
            abort(404)

        data = request.json
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            if email_validation(data['email']) is None:
                return jsonify({"error": "Invalid email format"}), 400
            user.email = data['email']

        db.session.commit()
        return jsonify({"success": "User profile updated successfully"}), 200
    abort(401)


# Change password
@users_bp.route(Config.CHANGE_PASSWORD, methods=['PUT'])
@jwt_required()
def change_password(user_id):
    if get_jwt_identity() == user_id:
        user = Users.query.get(user_id)
        if not user:
            abort(404)

        data = request.json
        if 'old_password' not in data or 'new_password' not in data:
            return jsonify({"error": "Missing fields"}), 400

        if not check_password_hash(user.pwd, data['old_password']):
            return jsonify({"error": "Old password does not match"}), 401

        if password_validation(data['new_password']) is None:
            return jsonify({"password_validation": error_pwd_validation_msg}), 400

        user.pwd = generate_password_hash(data['new_password'])
        db.session.commit()
        return jsonify({"success": "Password changed successfully"}), 200
    abort(401)


# Delete account
@users_bp.route(Config.DELETE_ACCOUNT, methods=['DELETE'])
@jwt_required()
def delete_account(user_id):
    if get_jwt_identity() == user_id:
        user = Users.query.get(user_id)
        if not user:
            abort(404)

        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "Account Deleted Successfully"}), 200
    abort(401)


# Sign-in
@users_bp.route(Config.SIGN_IN, methods=['POST'])
def sign_in():
    # if request.method == 'OPTIONS':
    # # Respond with empty OK for preflight
    #     return '', 200
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = Users.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.pwd, password):
        return jsonify({"error": "Incorrect Email or Password"}), 401

    access_token = create_access_token(identity="mri")
    return jsonify({
        "access_token": access_token,
        "name": user.name,
        "email": user.email
    }), 200


# Sign-up
@users_bp.route(Config.SIGN_UP, methods=['POST'])
def sign_up():
    data = request.json
    try:
        name = data['name']
        email = data['email']
        password = data['password']

        if Users.query.filter_by(email=email).first():
            return jsonify({"error": f"Email '{email}' already exists"}), 400

        if email_validation(email) is None:
            return jsonify({"email_validation": f"{email} is not a valid email address"}), 400

        if password_validation(password) is None:
            return jsonify({"password_validation": error_pwd_validation_msg}), 400

        hashed_password = generate_password_hash(password)

        user = Users(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            pwd=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": "User Created Successfully"}), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400


# Error Handlers
@users_bp.errorhandler(400)
def invalid_request(error):
    return jsonify({'error': 'Invalid Request'}), 400

@users_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'User not found'}), 404

@users_bp.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized Access'}), 401


# Utility: password validation
def password_validation(password):
    pwd_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    return re.search(pwd_regex, password)

# Utility: email validation
def email_validation(email):
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(email_regex, email)
