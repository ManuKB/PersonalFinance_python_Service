from flask import Blueprint, request, jsonify
from models import db, Price_History
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import abort
import uuid
from datetime import datetime
from config import Config

price_history_bp = Blueprint('price_history', __name__, url_prefix=Config.API_PATH+Config.API_VERSION+'/price_history/<string:appname>')

# ▶️ Create Price History
@price_history_bp.route('/', methods=['POST'])
@jwt_required()
def create_price_history(appname):
    if get_jwt_identity() != appname:
        abort(401)

    data = request.get_json()
    asset_id = data.get('asset_id')
    date_str = data.get('date')
    price = data.get('price')

    if not all([asset_id, date_str, price]):
        abort(400)

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    new_id = str(uuid.uuid4())
    history = Price_History(id=new_id, asset_id=asset_id, date=date, price=price)
    db.session.add(history)
    db.session.commit()

    return jsonify({"message": "Price history entry created.", "id": new_id}), 201


# 📥 Get All Price History
@price_history_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_price_history(appname):
    if get_jwt_identity() != appname:
        abort(401)

    records = Price_History.query.all()
    result = [
        {
            "id": r.id,
            "asset_id": r.asset_id,
            "date": r.date.strftime("%Y-%m-%d"),
            "price": str(r.price)
        } for r in records
    ]
    return jsonify(result), 200


# 🔍 Get by ID
@price_history_bp.route('/<string:id>/', methods=['GET'])
@jwt_required()
def get_price_history_by_id(id, appname):
    if get_jwt_identity() != appname:
        abort(401)

    record = Price_History.query.get(id)
    if not record:
        abort(404)

    return jsonify({
        "id": record.id,
        "asset_id": record.asset_id,
        "date": record.date.strftime("%Y-%m-%d"),
        "price": str(record.price)
    }), 200


# ✏️ Update Price History
@price_history_bp.route('/<string:id>/', methods=['PUT'])
@jwt_required()
def update_price_history(id, appname):
    if get_jwt_identity() != appname:
        abort(401)

    record = Price_History.query.get(id)
    if not record:
        abort(404)

    data = request.get_json()
    if "price" in data:
        record.price = data["price"]
    if "date" in data:
        try:
            record.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    db.session.commit()
    return jsonify({"message": "Price history updated."}), 200


# ❌ Delete Price History
@price_history_bp.route('/<string:id>/', methods=['DELETE'])
@jwt_required()
def delete_price_history(id, appname):
    if get_jwt_identity() != appname:
        abort(401)

    record = Price_History.query.get(id)
    if not record:
        abort(404)

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Price history deleted."}), 200


# Error handlers
@price_history_bp.errorhandler(400) # Bad Request   
def invalid_request(error):
    return jsonify({'error': 'Invalid request'}), 400   

@price_history_bp.errorhandler(404) # Not Found
def not_found(error):
    return jsonify({'error': 'Price history not found'}), 404       

@price_history_bp.errorhandler(401) # Unauthorized
def unauthorized(error):
    return jsonify({'error': 'Unauthorized access'}), 401

