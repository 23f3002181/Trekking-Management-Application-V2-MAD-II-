from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from models import db
from models.trek_models import Trek, Booking
from datetime import datetime

# Define the blueprint
user_bp = Blueprint('user_bp', __name__)

# 1. API to Fetch Open Treks (with Search and Filter)
@user_bp.route('/api/user/treks', methods=['GET'])
@auth_required('token')
@roles_required('trekker')
def get_open_treks():
    search = request.args.get('search', '').lower()
    difficulty = request.args.get('difficulty', '')

    # Base query: Only show 'Open' treks that have available slots
    query = Trek.query.filter(Trek.status == 'Open', Trek.available_slots > 0)

    if search:
        query = query.filter(Trek.name.ilike(f"%{search}%") | Trek.location.ilike(f"%{search}%"))
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    treks = query.all()
    
    trek_list = [{
        "id": t.id,
        "name": t.name,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration": t.duration_days,
        "slots": t.available_slots
    } for t in treks]
    
    return jsonify(trek_list), 200

# 2. API to Book a Trek
@user_bp.route('/api/user/book/<int:trek_id>', methods=['POST'])
@auth_required('token')
@roles_required('trekker')
def book_trek(trek_id):
    trek = Trek.query.get(trek_id)
    
    # Validation 1: Does the trek exist and is it open?
    if not trek or trek.status != 'Open' or trek.available_slots <= 0:
        return jsonify({"message": "Trek is currently unavailable for booking."}), 400
        
    # Validation 2: Has the user already booked this trek?
    existing_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek_id).first()
    if existing_booking:
        return jsonify({"message": "You have already booked this trek."}), 400

    # Create booking and reduce available slots
    new_booking = Booking(
        user_id=current_user.id,
        trek_id=trek_id,
        booking_date=datetime.utcnow(),
        status='Booked'
    )
    trek.available_slots -= 1
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({"message": "Trek booked successfully!"}), 201

# 3. API to Fetch User's Booking History
@user_bp.route('/api/user/bookings', methods=['GET'])
@auth_required('token')
@roles_required('trekker')
def get_my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    
    history = []
    for b in bookings:
        trek = Trek.query.get(b.trek_id)
        history.append({
            "booking_id": b.id,
            "trek_name": trek.name,
            "location": trek.location,
            "booking_date": b.booking_date.strftime("%Y-%m-%d"),
            "status": b.status,
            "trek_status": trek.status
        })
        
    return jsonify(history), 200