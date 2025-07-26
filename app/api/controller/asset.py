from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import abort
from app.models import db, Assets
from config import Config

assets_bp = Blueprint('assets', __name__, url_prefix=Config.API_PATH+Config.API_VERSION+'/assets/<string:appname>')

# Fetch all assets
@assets_bp.route('/', methods=['GET'])
@jwt_required()
def fetch_assets(appname):
    if get_jwt_identity() != appname:
        abort(401)

    assets = Assets.query.all()
    return jsonify([asset.to_dict() for asset in assets]), 200


# Search asset by title
@assets_bp.route('/<string:id>', methods=['GET'])
@jwt_required()
def search_asset(appname, id):
    if get_jwt_identity() != appname:
        abort(401)

    asset = Assets.query.filter_by(id=id).first()
    if not asset:
        abort(404)

    return jsonify(asset.to_dict()), 200


# Delete asset by title
@assets_bp.route('/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_asset(appname, id):
    if get_jwt_identity() != appname:
        abort(401)

    asset = Assets.query.filter_by(id=id).first()
    if not asset:
        abort(404)

    db.session.delete(asset)
    db.session.commit()
    return jsonify({"success": "asset deleted successfully"}), 200

# Add a new asset
@assets_bp.route('/', methods=['POST'])
@jwt_required()
def add_asset(appname):
    if get_jwt_identity() != appname:
        abort(401)

    try:
        data = request.json
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid data format"}), 400
        id = Assets.query.all().count() + 1
        data['id'] = str(id).zfill(5) # Assign a new ID for the asset
        asset = Assets(data)
        db.session.add(asset)
        db.session.commit()
        return jsonify({"success": "asset added successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

# Update an existing asset
@assets_bp.route('/<string:id>', methods=['PUT'])
@jwt_required()
def update_asset(appname, id):
    if get_jwt_identity() != appname:
        abort(401)

    try:
        data = request.json

        asset = Assets.query.filter_by(id=id).first()
        if not asset:
          abort(404)
        asset.name = data.get('name', asset.name)
        asset.symbol = data.get('symbol', asset.symbol)
        asset.investment_type = data.get('investment_type', asset.investment_type)
        asset.currency = data.get('currency', asset.currency)
        asset.platform = data.get('platform', asset.platform)
        asset.custom_data = data.get('custom_data', asset.custom_data)  
        db.session.commit()
        return jsonify({"success": "asset updated successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400


# Error handlers
@assets_bp.errorhandler(400)
def invalid_request(error):
    return jsonify({'error': 'Invalid request'}), 400

@assets_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'asset not found'}), 404

@assets_bp.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized access'}), 401
