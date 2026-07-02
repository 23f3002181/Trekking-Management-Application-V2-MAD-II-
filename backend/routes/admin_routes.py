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
            total_slots=data.get('total_slots'),
            available_slots=data.get('total_slots'),
            assigned_staff_id=data.get('staff_id') or None,
            status='Open'
        )
        db.session.add(new_trek)
        db.session.commit()
        cache.clear()
        return jsonify({"message": "Trek route created successfully"}), 201

    treks = Trek.query.all()
    staff_profiles = StaffProfile.query.all()
    
    trek_list = []
    for t in treks:
        # Fetch staff name if assigned
        staff = StaffProfile.query.get(t.assigned_staff_id) if t.assigned_staff_id else None
        
        trek_list.append({
            "id": t.id, 
            "name": t.name, 
            "location": t.location, 
            "difficulty": t.difficulty,
            "available_slots": t.available_slots,
            "total_slots": t.total_slots,
            "status": t.status,
            "staff_id": t.assigned_staff_id, # Added so Vue knows who is selected
            "staff_name": staff.name if staff else "Unassigned",
            "duration": t.duration_days,
            "start_date": t.start_date.strftime("%d-%m-%Y") if t.start_date else "TBD",
            "end_date": t.end_date.strftime("%d-%m-%Y") if t.end_date else "TBD"
        })
    
    staff_list = [{"id": s.id, "name": s.name} for s in staff_profiles]
    return jsonify({"treks": trek_list, "staff": staff_list}), 200

# NEW: API to Assign/Reassign Staff to a Trek
@admin_bp.route('/api/admin/treks/<int:trek_id>/assign', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def assign_trek_staff(trek_id):
    data = request.get_json()
    trek = Trek.query.get_or_404(trek_id)
    
    # Get the staff ID (can be None if admin is unassigning)
    staff_id = data.get('staff_id') 
    
    trek.assigned_staff_id = staff_id if staff_id else None
    db.session.commit()
    
    return jsonify({"message": "Staff assignment updated!"}), 200

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
    bookings = db.session.query(Booking, User, Trek)\
        .join(User, Booking.user_id == User.id)\
        .join(Trek, Booking.trek_id == Trek.id).all()
        
    history = []
    for b, u, t in bookings:
        history.append({
            "id": b.id,
            "user_name": u.full_name or "N/A",  
            "user_email": u.email,
            "trek_name": t.name,
            "booking_date": b.booking_date.strftime("%d-%m-%Y"), 
            "start_date": t.start_date.strftime("%d-%m-%Y") if t.start_date else "TBD",
            "end_date": t.end_date.strftime("%d-%m-%Y") if t.end_date else "TBD",
            "status": b.status
        })
    return jsonify(history), 200

# Edit a Trek
@admin_bp.route('/api/admin/treks/<int:trek_id>', methods=['PUT'])
@auth_required('token')
@roles_required('admin')
def edit_trek(trek_id):
    data = request.get_json()
    trek = Trek.query.get_or_404(trek_id)
    
    trek.name = data.get('name', trek.name)
    trek.location = data.get('location', trek.location)
    trek.difficulty = data.get('difficulty', trek.difficulty)
    trek.duration_days = data.get('duration', trek.duration_days)
    new_total_slots = int(data.get('total_slots', trek.total_slots))
    if new_total_slots != trek.total_slots:
        # If capacity goes up by 5, available slots goes up by 5. 
        # If capacity drops by 2, available drops by 2.
        slot_difference = new_total_slots - trek.total_slots
        trek.total_slots = new_total_slots
        trek.available_slots = trek.available_slots + slot_difference
    
    # Handle staff assignment changes from the edit form
    staff_id = data.get('staff_id')
    trek.assigned_staff_id = staff_id if staff_id else None
    
    db.session.commit()
    cache.clear()
    
    return jsonify({"message": "Trek updated successfully"}), 200

# Delete a Trek
@admin_bp.route('/api/admin/treks/<int:trek_id>', methods=['DELETE'])
@auth_required('token')
@roles_required('admin')
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    
    # Optional Security Check: Don't allow deletion if bookings exist
    if Booking.query.filter_by(trek_id=trek.id).first():
        return jsonify({"message": "Cannot delete trek because bookings exist."}), 400
        
    db.session.delete(trek)
    db.session.commit()
    cache.clear()
    
    return jsonify({"message": "Trek deleted successfully"}), 200

# Get Trek Participants
@admin_bp.route('/api/admin/treks/<int:trek_id>/participants', methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_trek_participants(trek_id):
    # Join Booking and User where the trek ID matches
    bookings = db.session.query(Booking, User)\
        .join(User, Booking.user_id == User.id)\
        .filter(Booking.trek_id == trek_id).all()
        
    participants = []
    for b, u in bookings:
        participants.append({
            "booking_id": b.id,
            "user_id": u.id,
            "name": u.full_name or "N/A",
            "email": u.email,
            "contact": u.contact or "N/A",
            "booking_date": b.booking_date.strftime("%Y-%m-%d"),
            "booking_status": b.status
        })
        
    return jsonify(participants), 200