from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from models import db
from models.trek_models import Trek, Booking
from models.user_models import User, StaffProfile

# Define the blueprint
staff_bp = Blueprint('staff_bp', __name__)

# 1. API to get Treks assigned to the logged-in staff member
@staff_bp.route('/api/staff/treks', methods=['GET'])
@auth_required('token')
@roles_required('staff')
def get_assigned_treks():
    # Find the staff profile linked to the current user
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    if not staff_profile:
        return jsonify({"message": "Staff profile not found."}), 404
        
    treks = Trek.query.filter_by(assigned_staff_id=staff_profile.id).all()
    
    trek_list = []
    for t in treks:
        # Count how many users have booked this specific trek
        participant_count = Booking.query.filter_by(trek_id=t.id, status='Booked').count()
        trek_list.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "difficulty": t.difficulty,
            "slots": t.available_slots,
            "status": t.status,
            "participants": participant_count
        })
        
    return jsonify(trek_list), 200

# 2. API to update Trek Slots and Status
@staff_bp.route('/api/staff/treks/<int:trek_id>', methods=['PUT'])
@auth_required('token')
@roles_required('staff')
def update_trek(trek_id):
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=staff_profile.id).first()
    
    if not trek:
        return jsonify({"message": "Trek not found or unauthorized."}), 403
        
    data = request.get_json()
    if 'slots' in data:
        trek.available_slots = int(data['slots'])
    if 'status' in data:
        trek.status = data['status']
        
        # NEW LOGIC: Cascade completion to bookings
        if trek.status == 'Completed':
            active_bookings = Booking.query.filter_by(trek_id=trek.id, status='Booked').all()
            for b in active_bookings:
                b.status = 'Completed'
                
    db.session.commit()
    return jsonify({"message": "Trek updated successfully"}), 200

# 3. API to view registered participants for a trek
@staff_bp.route('/api/staff/treks/<int:trek_id>/participants', methods=['GET'])
@auth_required('token')
@roles_required('staff')
def get_participants(trek_id):
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=staff_profile.id).first()
    
    if not trek:
        return jsonify({"message": "Unauthorized"}), 403
        
    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    participants = []
    for b in bookings:
        user = User.query.get(b.user_id)
        participants.append({
            "booking_id": b.id,
            "user_email": user.email,
            "booking_date": b.booking_date.strftime("%Y-%m-%d") if b.booking_date else "N/A",
            "status": b.status
        })
        
    return jsonify(participants), 200