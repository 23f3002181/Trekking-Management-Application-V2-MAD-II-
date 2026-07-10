from flask import Blueprint, request, jsonify, current_app
from flask_security import verify_password, login_user, logout_user, auth_required
from flask_security.utils import hash_password
from models import db
import uuid

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    datastore = current_app.extensions['security'].datastore
    user = datastore.find_user(email=email)
    
    if user and verify_password(password, user.password):
        # blacklist check
        if not user.active:
            return jsonify({"message": "Your account has been blacklisted. Please contact the administrator."}), 403
            
        login_user(user)
        role = 'trekker'
        if user.has_role('admin'): role = 'admin'
        elif user.has_role('staff'): role = 'staff'
            
        return jsonify({"message": "Login successful", "token": user.get_auth_token(), "role": role}), 200
        
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    contact = data.get('contact')

    datastore = current_app.extensions['security'].datastore

    if datastore.find_user(email=email):
        return jsonify({"message": "Email already exists"}), 400

    datastore.create_user(
        email=email, 
        password=hash_password(password),
        fs_uniquifier=str(uuid.uuid4()),
        full_name=full_name,
        contact=contact,
        roles=['trekker']
    )
    db.session.commit()
    return jsonify({"message": "Trekker registered successfully"}), 201

@auth_bp.route('/api/logout', methods=['POST'])
@auth_required('token')
def api_logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200