from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from models import db
from models.trek_models import Trek, Booking
from models.user_models import User, StaffProfile
from cache import cache
from datetime import datetime
import pytz

staff_bp = Blueprint('staff_bp', __name__)

def get_staff_profile():
    return StaffProfile.query.filter_by(user_id=current_user.id).first()

# 1. API for Dashboard Stats (Screen 8 Top Cards)
@staff_bp.route('/api/staff/stats', methods=['GET'])
@auth_required('token')
@roles_required('staff')
def get_staff_stats():
    staff_profile = get_staff_profile()
    if not staff_profile:
        return jsonify({"message": "Staff profile not found."}), 404
        
    treks = Trek.query.filter_by(assigned_staff_id=staff_profile.id).all()
    assigned_treks_count = len(treks)
    ongoing_treks_count = len([t for t in treks if t.status == 'Open'])
    
    trek_ids = [t.id for t in treks]
    total_participants = Booking.query.filter(Booking.trek_id.in_(trek_ids), Booking.status == 'Booked').count() if trek_ids else 0

    return jsonify({
        "assigned_treks": assigned_treks_count,
        "total_participants": total_participants,
        "ongoing_treks": ongoing_treks_count
    }), 200

# 2. API to get Treks list (Screen 8 Table)
@staff_bp.route('/api/staff/treks', methods=['GET'])
@auth_required('token')
@roles_required('staff')
def get_assigned_treks():
    staff_profile = get_staff_profile()
    treks = Trek.query.filter_by(assigned_staff_id=staff_profile.id).all()
    
    trek_list = []
    for t in treks:
        participant_count = Booking.query.filter_by(trek_id=t.id, status='Booked').count()
        trek_list.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "difficulty": t.difficulty,
            "slots": t.available_slots,
            "total_slots": t.total_slots,
            "status": t.status,
            "participants": participant_count,
            "start_date": t.start_date.strftime("%d %b %Y") if t.start_date else "TBA",
            "end_date": t.end_date.strftime("%d %b %Y") if t.end_date else "TBA"
        })
    return jsonify(trek_list), 200

# 3. API to get a single Trek's details (Screen 9 Left Side)
@staff_bp.route('/api/staff/treks/<int:trek_id>', methods=['GET'])
@auth_required('token')
@roles_required('staff')
def get_single_trek(trek_id):
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=staff_profile.id).first()
    
    if not trek:
        return jsonify({"message": "Trek not found or unauthorized."}), 403

    return jsonify({
        "id": trek.id,
        "name": trek.name,
        "difficulty": trek.difficulty,
        "duration": trek.duration_days,
        "total_slots": trek.total_slots,
        "available_slots": trek.available_slots,
        "status": trek.status,
        # Format as YYYY-MM-DD for HTML date inputs
        "start_date": trek.start_date.strftime("%Y-%m-%d") if trek.start_date else "",
        "end_date": trek.end_date.strftime("%Y-%m-%d") if trek.end_date else ""
    }), 200

# 4. API to view registered participants (Screen 9 Right Side)
@staff_bp.route('/api/staff/treks/<int:trek_id>/participants', methods=['GET'])
@auth_required('token')
@roles_required('staff')
def get_participants(trek_id):
    staff_profile = get_staff_profile()
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=staff_profile.id).first()
    if not trek:
        return jsonify({"message": "Unauthorized"}), 403
        
    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    participants = []
    for index, b in enumerate(bookings, start=1):
        user = User.query.get(b.user_id)
        participants.append({
            "index": index,
            "booking_id": b.id,
            "user_name": user.full_name or "Trekker",
            "user_email": user.email,
            "booking_date": b.booking_date.strftime("%d %b %Y") if b.booking_date else "N/A",
            "status": b.status
        })
    return jsonify(participants), 200

# 5. API to update Trek Status and Slots
@staff_bp.route('/api/staff/treks/<int:trek_id>', methods=['PUT'])
@auth_required('token')
@roles_required('staff')
def update_trek(trek_id):
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=staff_profile.id).first()
    
    if not trek:
        return jsonify({"message": "Unauthorized"}), 403
        
    data = request.get_json()
    ist = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist).date()
    
    # 1. Update Dates with Strict Validation
    if 'start_date' in data and data['start_date']:
        new_start = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        
        # Block past dates (unless the trek was already started previously)
        if new_start < today and trek.status != 'Started':
            return jsonify({"message": "Start date cannot be in the past."}), 400
            
        trek.start_date = new_start

    if 'end_date' in data and data['end_date']:
        new_end = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        # Block end dates that occur before the start date
        if trek.start_date and new_end < trek.start_date:
            return jsonify({"message": "End date cannot be earlier than the start date."}), 400
            
        trek.end_date = new_end
        
    # 2. Update Slots
    if 'total_slots' in data:
        new_total = int(data['total_slots'])
        booked_count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        trek.total_slots = new_total
        trek.available_slots = new_total - booked_count

    # 3. Update Status
    if 'status' in data:
        trek.status = data['status']
        if trek.status == 'Completed':
            active_bookings = Booking.query.filter_by(trek_id=trek.id, status='Booked').all()
            for b in active_bookings:
                b.status = 'Completed'
                
    db.session.commit()
    return jsonify({
        "message": "Trek updated successfully",
        "available_slots": trek.available_slots
    }), 200

# 6. API for Completed Bookings History (Independent of Trek Status)
@staff_bp.route('/api/staff/history', methods=['GET'])
@auth_required('token')
@roles_required('staff')
def get_staff_history():
    # 1. Get the current staff member
    staff_profile = StaffProfile.query.filter_by(user_id=current_user.id).first()
    if not staff_profile:
        return jsonify({"message": "Unauthorized"}), 403

    # 2. Find all treks assigned to this staff
    treks = Trek.query.filter_by(assigned_staff_id=staff_profile.id).all()
    trek_ids = [t.id for t in treks]

    # 3. Fetch ONLY 'Completed' bookings for these specific treks
    completed_bookings = Booking.query.filter(
        Booking.trek_id.in_(trek_ids), 
        Booking.status == 'Completed'
    ).all()

    # 4. Format the response
    history = []
    for b in completed_bookings:
        user = User.query.get(b.user_id)
        trek = next((t for t in treks if t.id == b.trek_id), None)
        
        history.append({
            "booking_id": b.id,
            "trek_name": trek.name if trek else "Unknown",
            "user_name": user.full_name or "Trekker",
            "user_email": user.email,
            "booking_date": b.booking_date.strftime("%d %b %Y") if b.booking_date else "N/A",
            "status": b.status
        })

    return jsonify(history), 200