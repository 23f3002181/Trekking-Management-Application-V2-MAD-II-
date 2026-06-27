from flask import Blueprint, request, jsonify, current_app
from flask_security import auth_required, roles_required
from flask_security.utils import hash_password
from models import db
from models.user_models import User, StaffProfile
from models.trek_models import Trek, Booking
from cache import cache
import uuid

admin_bp = Blueprint('admin_bp', __name__)

# --- TREK MANAGEMENT ---
@admin_bp.route('/api/admin/treks', methods=['GET', 'POST'])
@auth_required('token')
@roles_required('admin')
def manage_treks():
    if request.method == 'POST':
        data = request.get_json()
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
    
    return jsonify({"treks": trek_list, "staff": staff_list}), 200

# --- DASHBOARD STATS ---
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

# --- STAFF MANAGEMENT ---
@admin_bp.route('/api/admin/staff', methods=['GET', 'POST'])
@auth_required('token')
@roles_required('admin')
def manage_staff():
    if request.method == 'POST':
        data = request.get_json()
        datastore = current_app.extensions['security'].datastore

        if datastore.find_user(email=data.get('email')):
            return jsonify({"message": "Email already exists"}), 400

        user = datastore.create_user(
            email=data.get('email'), 
            password=hash_password(data.get('password')),
            fs_uniquifier=str(uuid.uuid4()),
            roles=['staff'],
            active=True
        )
        db.session.flush() 

        new_staff = StaffProfile(user_id=user.id, name=data.get('name'), contact_details=data.get('contact'))
        db.session.add(new_staff)
        db.session.commit()
        return jsonify({"message": "Trek Staff created successfully"}), 201
    
    # GET Request: Fetch Staff List with Status
    staff_profiles = StaffProfile.query.all()
    staff_data = []
    for sp in staff_profiles:
        user = User.query.get(sp.user_id)
        staff_data.append({
            "id": sp.id,
            "user_id": user.id,
            "name": sp.name,
            "email": user.email,
            "contact": sp.contact_details,
            "active": user.active
        })
    return jsonify(staff_data), 200

# --- USER (TREKKER) MANAGEMENT ---
@admin_bp.route('/api/admin/users', methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_all_users():
    # Fetch all users who have the 'trekker' role
    users = User.query.filter(User.roles.any(name='trekker')).all()
    user_data = []
    for u in users:
        user_data.append({
            "id": u.id,
            "name": u.full_name or "N/A",  # Added full_name
            "email": u.email,
            "contact": u.contact or "N/A", # Added contact
            "active": u.active
        })
    return jsonify(user_data), 200

# --- TOGGLE ACTIVE/BLACKLIST STATUS ---
@admin_bp.route('/api/admin/users/<int:user_id>/toggle-status', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.active = not user.active  # Toggle the boolean
    db.session.commit()
    status_text = "whitelisted" if user.active else "blacklisted"
    return jsonify({"message": f"User successfully {status_text}."}), 200

# --- BOOKINGS ---
@admin_bp.route('/api/admin/bookings', methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_all_bookings():
    # Optimized Join Query to prevent N+1 DB calls
    bookings = db.session.query(Booking, User, Trek)\
        .join(User, Booking.user_id == User.id)\
        .join(Trek, Booking.trek_id == Trek.id)\
        .all()
        
    history = []
    for b, u, t in bookings:
        history.append({
            "id": b.id,
            "user_email": u.email,
            "trek_name": t.name,
            "date": b.booking_date.strftime("%Y-%m-%d"),
            "status": b.status
        })
    return jsonify(history), 200