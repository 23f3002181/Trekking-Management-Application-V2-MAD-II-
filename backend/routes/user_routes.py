import os

from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from models import db
from models.trek_models import Trek, Booking
from datetime import datetime
from flask import send_file
from cache import cache
from sqlalchemy import func

user_bp = Blueprint('user_bp', __name__)

# Fetch Open Treks
@user_bp.route('/api/user/treks', methods=['GET'])
@auth_required('token')
@roles_required('trekker')
@cache.cached(timeout=60, query_string=True)
def get_open_treks():
    print("Fetching treks from the Database...")
    search = request.args.get('search', '').lower()
    difficulty = request.args.get('difficulty', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)
    query = Trek.query.filter(Trek.status == 'Open', Trek.available_slots > 0)
    if search:
        query = query.filter(Trek.name.ilike(f"%{search}%") | Trek.location.ilike(f"%{search}%"))
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    treks = pagination.items # Get just the items for the current page
    
    trek_list = [{
        "id": t.id,
        "name": t.name,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration": t.duration_days,
        "slots": t.available_slots,
        "start_date": t.start_date.strftime("%d %b %Y") if t.start_date else "TBD",
        "end_date": t.end_date.strftime("%d %b %Y") if t.end_date else "TBD",
        "image_url": f"http://127.0.0.1:5000/static/uploads/{t.image_filename}" if t.image_filename else "https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&auto=format&fit=crop&q=60"
    } for t in treks]

    return jsonify({
        "treks": trek_list,
        "current_page": pagination.page,
        "total_pages": pagination.pages,
        "total_items": pagination.total
    }), 200

# Book a Trek
@user_bp.route('/api/user/book/<int:trek_id>', methods=['POST'])
@auth_required('token')
@roles_required('trekker')
def book_trek(trek_id):
    trek = Trek.query.get(trek_id)

    if not trek or trek.status != 'Open' or trek.available_slots <= 0:
        return jsonify({"message": "Trek is currently unavailable for booking."}), 400
        
    existing_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek_id).first()
    
    if existing_booking:
        if existing_booking.status == 'Booked':
            return jsonify({"message": "You have already booked this trek."}), 400
        elif existing_booking.status == 'Completed':
            return jsonify({"message": "You have already completed this trek."}), 400
        elif existing_booking.status == 'Cancelled':
            existing_booking.status = 'Booked'
            existing_booking.booking_date = datetime.utcnow()
            trek.available_slots -= 1
            db.session.commit()
            cache.clear()
        
            return jsonify({"message": "Trek booked successfully!"}), 201

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

# Fetch user's booking history
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
            "booking_date": b.booking_date.strftime("%d %b %Y") if b.booking_date else "N/A",
            "status": b.status,
            "trek_status": trek.status,
            "start_date": trek.start_date.strftime("%d %b %Y") if trek.start_date else "TBD",
            "end_date": trek.end_date.strftime("%d %b %Y") if trek.end_date else "TBD"
        })
        
    return jsonify(history), 200

# Cancel a Booking
@user_bp.route('/api/user/bookings/<int:booking_id>/cancel', methods=['PUT'])
@auth_required('token')
@roles_required('trekker')
def cancel_booking(booking_id):
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first()
    if not booking or booking.status != 'Booked':
        return jsonify({"message": "Invalid booking or already cancelled/completed."}), 400
    booking.status = 'Cancelled'
    trek = Trek.query.get(booking.trek_id)
    if trek:
        trek.available_slots += 1
        
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Booking cancelled successfully."}), 200

# export booking history to CSV
@user_bp.route('/api/user/export', methods=['POST'])
@auth_required('token')
@roles_required('trekker')
def trigger_export():
    from tasks import export_booking_history_csv
    task = export_booking_history_csv.delay(current_user.id)
    return jsonify({"message": "Export started!", "task_id": task.id}), 202

@user_bp.route('/api/user/export/status/<task_id>', methods=['GET'])
@auth_required('token')
@roles_required('trekker')
def export_status(task_id):
    from app import celery 
    task_result = celery.AsyncResult(task_id)
    
    if task_result.state == 'SUCCESS':
        file_path = task_result.result
        import os
        absolute_path = os.path.abspath(file_path)
        return send_file(absolute_path, as_attachment=True, max_age=0)
        
    elif task_result.state == 'FAILURE':
        return jsonify({"status": "Failed"}), 500
    else:
        return jsonify({"status": "Processing"}), 202
    
@user_bp.route('/api/public/analytics', methods=['GET'])
def public_analytics():
    popular_treks = db.session.query(
        Trek.name, func.count(Booking.id), Trek.image_filename
    ).outerjoin(Booking, Trek.id == Booking.trek_id) \
     .group_by(Trek.id) \
     .order_by(func.count(Booking.id).desc()) \
     .limit(5).all()

    trek_names = [t[0] for t in popular_treks]
    trek_counts = [t[1] for t in popular_treks]
    
    DEFAULT_IMAGE = "https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&auto=format&fit=crop&q=60"
    trek_images = [
        f"http://127.0.0.1:5000/static/uploads/{t[2]}" if t[2] else DEFAULT_IMAGE
        for t in popular_treks
    ]
    status_counts = db.session.query(
        Trek.status, func.count(Trek.id)
    ).group_by(Trek.status).all()

    statuses = [s[0] for s in status_counts]
    status_values = [s[1] for s in status_counts]
    all_bookings = db.session.query(Booking.booking_date).filter(
        Booking.status.in_(['Booked', 'Completed'])
    ).all()
    
    monthly_trends = {}
    for b in all_bookings:
        if b.booking_date:
            date_str = b.booking_date.strftime('%Y-%m') 
            monthly_trends[date_str] = monthly_trends.get(date_str, 0) + 1
            
    sorted_months = sorted(monthly_trends.keys())
    trend_labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in sorted_months]
    trend_data = [monthly_trends[m] for m in sorted_months]

    return jsonify({
        "popular_treks": {
            "labels": trek_names,
            "data": trek_counts,
            "images": trek_images
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

# Fetch Profile Data
@user_bp.route('/api/user/profile', methods=['GET'])
@auth_required('token')
def get_profile():
    return jsonify({
        "full_name": current_user.full_name or "",
        "email": current_user.email,
        "contact": current_user.contact or ""
    }), 200

# Update profile
@user_bp.route('/api/user/profile', methods=['PUT'])
@auth_required('token')
def update_profile():
    data = request.get_json()
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    if 'contact' in data:
        current_user.contact = data['contact']
        
    db.session.commit()
    
    return jsonify({"message": "Profile updated successfully!"}), 200