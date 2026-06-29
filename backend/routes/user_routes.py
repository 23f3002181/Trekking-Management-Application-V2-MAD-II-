import os

from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from models import db
from models.trek_models import Trek, Booking
from datetime import datetime
from flask import send_file
from cache import cache
from sqlalchemy import func

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
    
    # NEW: Get pagination parameters from the URL, defaulting to page 1 and 6 items per page
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)

    # Base query
    query = Trek.query.filter(Trek.status == 'Open', Trek.available_slots > 0)

    # Apply filters
    if search:
        query = query.filter(Trek.name.ilike(f"%{search}%") | Trek.location.ilike(f"%{search}%"))
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    # NEW: Paginate the query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    treks = pagination.items # Get just the items for the current page
    
    trek_list = [{
        "id": t.id,
        "name": t.name,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration": t.duration_days,
        "slots": t.available_slots
    } for t in treks]
    
    # NEW: Return the list wrapped in a dictionary with the pagination metadata
    return jsonify({
        "treks": trek_list,
        "current_page": pagination.page,
        "total_pages": pagination.pages,
        "total_items": pagination.total
    }), 200

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
            cache.clear()
        
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
    # FIX 1: Import your specific celery instance, not the generic one
    from app import celery 
    
    # Check the result against YOUR Redis database
    task_result = celery.AsyncResult(task_id)
    
    if task_result.state == 'SUCCESS':
        # Provide the file download to the user
        file_path = task_result.result
        
        import os
        absolute_path = os.path.abspath(file_path)
        
        # Add max_age=0 to prevent the browser from holding onto this file
        return send_file(absolute_path, as_attachment=True, max_age=0)
        
    elif task_result.state == 'FAILURE':
        return jsonify({"status": "Failed"}), 500
    else:
        return jsonify({"status": "Processing"}), 202
    
# 7. Public Analytics API
@user_bp.route('/api/public/analytics', methods=['GET'])
def public_analytics():
    # 1. Most Popular Treks (Top 5 by number of bookings)
    popular_treks = db.session.query(
        Trek.name, func.count(Booking.id)
    ).outerjoin(Booking, Trek.id == Booking.trek_id) \
     .group_by(Trek.id) \
     .order_by(func.count(Booking.id).desc()) \
     .limit(5).all()

    trek_names = [t[0] for t in popular_treks]
    trek_counts = [t[1] for t in popular_treks]

    # 2. Trek Status Distribution
    status_counts = db.session.query(
        Trek.status, func.count(Trek.id)
    ).group_by(Trek.status).all()

    statuses = [s[0] for s in status_counts]
    status_values = [s[1] for s in status_counts]

    # 3. NEW: Monthly Booking Trends (Participation Statistics)
    # Fetch all non-cancelled bookings
    all_bookings = db.session.query(Booking.booking_date).filter(
        Booking.status.in_(['Booked', 'Completed'])
    ).all()
    
    monthly_trends = {}
    
    # Group by Year-Month (e.g., '2026-06')
    for b in all_bookings:
        if b.booking_date:
            date_str = b.booking_date.strftime('%Y-%m') 
            monthly_trends[date_str] = monthly_trends.get(date_str, 0) + 1
            
    # Sort chronologically and format for the frontend
    sorted_months = sorted(monthly_trends.keys())
    trend_labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in sorted_months]
    trend_data = [monthly_trends[m] for m in sorted_months]

    return jsonify({
        "popular_treks": {
            "labels": trek_names,
            "data": trek_counts
        },
        "trek_status": {
            "labels": statuses,
            "data": status_values
        },
        "booking_trends": {
            "labels": trend_labels,
            "data": trend_data
        }
    }), 200

# 8. API to Fetch Profile Data
@user_bp.route('/api/user/profile', methods=['GET'])
@auth_required('token')
def get_profile():
    # current_user is provided by Flask-Security
    return jsonify({
        "full_name": current_user.full_name or "",
        "email": current_user.email,
        "contact": current_user.contact or ""
    }), 200

# 9. API to Update Profile Data
@user_bp.route('/api/user/profile', methods=['PUT'])
@auth_required('token')
def update_profile():
    data = request.get_json()
    
    # Update the fields if they are provided in the request
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    if 'contact' in data:
        current_user.contact = data['contact']
        
    db.session.commit()
    
    return jsonify({"message": "Profile updated successfully!"}), 200