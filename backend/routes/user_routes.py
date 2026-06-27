from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from models import db
from models.trek_models import Trek, Booking
from datetime import datetime
from flask import send_file
from cache import cache
import os

# Define the blueprint
user_bp = Blueprint('user_bp', __name__)

# 1. API to Fetch Open Treks (with Search and Filter)
@user_bp.route('/api/user/treks', methods=['GET'])
@auth_required('token')
@roles_required('trekker')
@cache.cached(timeout=60, query_string=True)
def get_open_treks():
    print("Fetching treks from the Database...")
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
        
    # Validation 2: Check for existing bookings
    existing_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek_id).first()
    
    if existing_booking:
        if existing_booking.status == 'Booked':
            return jsonify({"message": "You have already booked this trek."}), 400
        elif existing_booking.status == 'Completed':
            return jsonify({"message": "You have already completed this trek."}), 400
        elif existing_booking.status == 'Cancelled':
            # REACTIVATE THE CANCELLED BOOKING
            existing_booking.status = 'Booked'
            existing_booking.booking_date = datetime.utcnow()
            trek.available_slots -= 1
            db.session.commit()
        
            return jsonify({"message": "Trek booked successfully!"}), 201

    # If no record exists at all, create a brand new one
    new_booking = Booking(
        user_id=current_user.id,
        trek_id=trek_id,
        booking_date=datetime.utcnow(),
        status='Booked'
    )
    trek.available_slots -= 1
    
    db.session.add(new_booking)
    db.session.commit()
    cache.clear() 
    
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

# 4. API to Cancel a Booking
@user_bp.route('/api/user/bookings/<int:booking_id>/cancel', methods=['PUT'])
@auth_required('token')
@roles_required('trekker')
def cancel_booking(booking_id):
    # Ensure the booking belongs to this user and is currently 'Booked'
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first()
    if not booking or booking.status != 'Booked':
        return jsonify({"message": "Invalid booking or already cancelled/completed."}), 400

    # Update status to Cancelled
    booking.status = 'Cancelled'
    
    # Free up the slot in the Trek
    trek = Trek.query.get(booking.trek_id)
    if trek:
        trek.available_slots += 1
        
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Booking cancelled successfully."}), 200

# 5. API to trigger the background job
@user_bp.route('/api/user/export', methods=['POST'])
@auth_required('token')
@roles_required('trekker')
def trigger_export():
    from tasks import export_booking_history_csv
    # The .delay() method tells Celery to run this in the background!
    task = export_booking_history_csv.delay(current_user.id)
    return jsonify({"message": "Export started!", "task_id": task.id}), 202

# 6. API to check status and download the file
@user_bp.route('/api/user/export/status/<task_id>', methods=['GET'])
@auth_required('token')
@roles_required('trekker')
def export_status(task_id):
    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'SUCCESS':
        # Provide the file download to the user
        file_path = task_result.result
        return send_file(os.path.join('..', file_path), as_attachment=True)
    elif task_result.state == 'FAILURE':
        return jsonify({"status": "Failed"}), 500
    else:
        return jsonify({"status": "Processing"}), 202