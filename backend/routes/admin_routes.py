from flask import Blueprint, request, jsonify, current_app
from flask_security import auth_required, roles_required
from flask_security.utils import hash_password
from models import db
from models.user_models import User, StaffProfile
from models.trek_models import Trek, Booking
from cache import cache
import uuid

# Define the blueprint
admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/api/admin/treks', methods=['GET', 'POST'])
@auth_required('token')
@roles_required('admin')
def manage_treks():
    if request.method == 'POST':
        data = request.get_json()
        
        # Create a new Trek
        new_trek = Trek(
            name=data.get('name'),
            location=data.get('location'),
            difficulty=data.get('difficulty'),
            duration_days=data.get('duration'),
            available_slots=data.get('slots'),
            assigned_staff_id=data.get('staff_id') or None,
            status='Open'
        )
        db.session.add(new_trek)
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Trek route created successfully"}), 201

    # If GET request, return all treks and staff (for the assignment dropdown)
    treks = Trek.query.all()
    staff_profiles = StaffProfile.query.all()
    
    trek_list = [{
        "id": t.id, 
        "name": t.name, 
        "location": t.location, 
        "difficulty": t.difficulty,
        "slots": t.available_slots,
        "status": t.status
    } for t in treks]
    
    staff_list = [{"id": s.id, "name": s.name} for s in staff_profiles]
    
    return jsonify({
        "treks": trek_list, 
        "staff": staff_list
    }), 200

# 1. API to get Dashboard Statistics
@admin_bp.route('/api/admin/stats', methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_stats():
    total_treks = Trek.query.count()
    total_users = User.query.filter(User.roles.any(name='trekker')).count()
    total_staff = User.query.filter(User.roles.any(name='staff')).count()
    total_bookings = Booking.query.count()
    
    return jsonify({
        "total_treks": total_treks,
        "total_users": total_users,
        "total_staff": total_staff,
        "total_bookings": total_bookings
    }), 200

# 2. API to Create Trek Staff
@admin_bp.route('/api/admin/staff', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def create_staff():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    contact = data.get('contact')

    datastore = current_app.extensions['security'].datastore

    if datastore.find_user(email=email):
        return jsonify({"message": "Email already exists"}), 400

    # Create the user account
    user = datastore.create_user(
        email=email, 
        password=hash_password(password),
        fs_uniquifier=str(uuid.uuid4()),
        roles=['staff']
    )
    db.session.flush() # Flush to get the new user.id before committing

    # Create the linked Staff Profile
    new_staff = StaffProfile(user_id=user.id, name=name, contact_details=contact)
    db.session.add(new_staff)
    db.session.commit()

    return jsonify({"message": "Trek Staff created successfully"}), 201

# 3. API to Fetch All Bookings
@admin_bp.route('/api/admin/bookings', methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_all_bookings():
    bookings = Booking.query.all()
    history = []
    for b in bookings:
        user = User.query.get(b.user_id)
        trek = Trek.query.get(b.trek_id)
        history.append({
            "id": b.id,
            "user_email": user.email,
            "trek_name": trek.name,
            "date": b.booking_date.strftime("%Y-%m-%d"),
            "status": b.status
        })
    return jsonify(history), 200