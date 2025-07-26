from flask import Blueprint, request, jsonify
from ...models import db, Constants
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import abort
from config import Config

constants_bp = Blueprint('constants', __name__, url_prefix=Config.API_PATH+Config.API_VERSION+'/constants/<string:appname>')


# ▶️ Create Constant
@constants_bp.route('/', methods=['POST'])
@jwt_required()
def create_constant(appname):
    if get_jwt_identity() != appname:
        abort(401)
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    if not name:
       abort(400)

    if Constants.query.get(name):
        return jsonify({"error": "Constant already exists"}), 409

    constant = Constants(name=name, description=description)
    db.session.add(constant)
    db.session.commit()

    return jsonify({"message": "Constant created", "data": {"name": name, "description": description}}), 201


# 📥 Get All Constants
@constants_bp.route('/', methods=['GET'])
@jwt_required()
def get_constants(appname):
    if get_jwt_identity() != appname:
        abort(401)
    constants = Constants.query.all()
    result = [{"name": c.name, "description": c.description} for c in constants]
    return jsonify(result), 200


# 🔍 Get Constant by Name
@constants_bp.route('/<string:name>/', methods=['GET'])
@jwt_required()
def get_constant(name, appname):
    if get_jwt_identity() != appname:
        abort(401)
    constant = Constants.query.get(name)
    if not constant:
        return jsonify({"error": "Constant not found"}), 404
    return jsonify({"name": constant.name, "description": constant.description}), 200


# ✏️ Update Constant
@constants_bp.route('/<string:name>/', methods=['PUT'])
@jwt_required()
def update_constant(name, appname):
    if get_jwt_identity() != appname:
        abort(401)
    constant = Constants.query.get(name)
    if not constant:
        return jsonify({"error": "Constant not found"}), 404

    data = request.get_json()
    constant.description = data.get('description', constant.description)
    db.session.commit()

    return jsonify({"message": "Constant updated", "data": {"name": constant.name, "description": constant.description}}), 200


# ❌ Delete Constant
@constants_bp.route('/<string:name>/', methods=['DELETE'])
@jwt_required()
def delete_constant(name, appname):
    if get_jwt_identity() != appname:
        abort(401)
    constant = Constants.query.get(name)
    if not constant:
        return jsonify({"error": "Constant not found"}), 404

    db.session.delete(constant)
    db.session.commit()
    return jsonify({"message": "Constant deleted"}), 200



# Error handlers
@constants_bp.errorhandler(400)
def invalid_request(error):
    return jsonify({'error': 'Invalid request'}), 400

@constants_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'asset not found'}), 404

@constants_bp.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized access'}), 401