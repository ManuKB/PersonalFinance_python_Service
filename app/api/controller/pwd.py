from flask import Blueprint, request, jsonify
import uuid
import app
from ...models import db, pwd
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import abort
from config import Config
from cryptography.fernet import Fernet

pwd_bp = Blueprint('pwds', __name__, url_prefix=Config.API_PATH+Config.API_VERSION+'/pwd/<string:appname>')
cipher = Fernet(Config.CIPHER_KEY)

# ▶️ Create pwd
@pwd_bp.route('/', methods=['POST'])
@jwt_required()
def create_pwd(appname):
    if get_jwt_identity() != appname:
        abort(401)
    data = request.get_json()
    entity = data.get('entity')
    pwd = data.get('pwd', '')
    pwd = cipher.encrypt(pwd.encode())
    new_id = str(uuid.uuid4())
    if not entity:
       abort(400)

    if pwd.query.get(entity):
        return jsonify({"error": "pwd already exists"}), 409

    p = pwd(id=new_id, entity=entity, pwd=pwd)
    db.session.add(p)
    db.session.commit()

    return jsonify({"message": "pwd created", "data": {"entity": entity, "pwd": pwd}}), 201


# 📥 Get All pwd
@pwd_bp.route('/', methods=['GET'])
@jwt_required()
def get_pwds(appname):
    if get_jwt_identity() != appname:
        abort(401)
    pwds = pwd.query.all()
    if not pwds:
        return jsonify({"message": "No constants found"}), 404
    # Decrypt passwords before returning
    for c in pwds:
        c.pwd = cipher.decrypt(c.pwd).decode()  
    result = [{"entity": c.entity, "pwd": c.pwd} for c in pwds]
    return jsonify(result), 200


# 🔍 Get pwd by Name
@pwd_bp.route('/<string:entity>/', methods=['GET'])
@jwt_required()
def get_pwd(entity, appname):
    if get_jwt_identity() != appname:
        abort(401)
    p = pwd.query.get(entity)
    if not p:
        return jsonify({"error": "pwd not found"}), 404
    # Decrypt password before returning
    p.pwd = cipher.decrypt(p.pwd).decode()
    return jsonify({"entity": p.entity, "pwd": p.pwd}), 200


# ✏️ Update pwd
@pwd_bp.route('/<string:entity>/', methods=['PUT'])
@jwt_required()
def update_pwd(entity, appname):
    if get_jwt_identity() != appname:
        abort(401)
    p = pwd.query.get(entity)
    if not p:
        return jsonify({"error": "pwd not found"}), 404

    data = request.get_json()
    pwd = data.get('pwd')
    if pwd:
        p.pwd = cipher.encrypt(pwd.encode())
    else:
        p.pwd = p.pwd
            
    db.session.commit()

    return jsonify({"message": "pwd updated", "data": {"entity": p.entity, "pwd": p.pwd}}), 200


# ❌ Delete pwd
@pwd_bp.route('/<string:entity>/', methods=['DELETE'])
@jwt_required()
def delete_pwd(entity, appname):
    if get_jwt_identity() != appname:
        abort(401)
    p = pwd.query.get(entity)
    if not p:
        return jsonify({"error": "pwd not found"}), 404

    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "pwd deleted"}), 200



# Error handlers
@pwd_bp.errorhandler(400)
def invalid_request(error):
    return jsonify({'error': 'Invalid request'}), 400

@pwd_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'asset not found'}), 404

@pwd_bp.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized access'}), 401