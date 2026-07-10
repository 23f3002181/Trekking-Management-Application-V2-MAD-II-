from app import celery
from models import db
from datetime import datetime, timedelta
from models.trek_models import Trek, Booking
from models.user_models import User
import csv
import os

@celery.task
def export_booking_history_csv(user_id):
    print(f"Starting async CSV export for User ID: {user_id}...")

    bookings = Booking.query.filter_by(user_id=user_id).all()

    export_dir = os.path.join('static', 'exports')
    os.makedirs(export_dir, exist_ok=True)

    filename = f"booking_history_{user_id}.csv"
    filepath = os.path.join(export_dir, filename)

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Booking ID', 'Trek Name', 'Location', 'Booking Date', 'Trek Dates', 'Status'])
        
        for b in bookings:
            trek = Trek.query.get(b.trek_id)
            writer.writerow([
                b.id, 
                trek.name, 
                trek.location, 
                b.booking_date.strftime("%Y-%m-%d"), 
                f"{trek.start_date.strftime('%d %b %Y') if trek.start_date else 'TBD'} - {trek.end_date.strftime('%d %b %Y') if trek.end_date else 'TBD'}",
                b.status
            ])
            
    print(f"Export complete! Saved to {filepath}")
    return filepath

@celery.task
def send_daily_reminders():
    print("\n--- RUNNING DAILY REMINDER JOB ---")
    bookings = Booking.query.filter_by(status='Booked').all()
    
    if not bookings:
        print("No active bookings to send reminders for.")
        return "No reminders needed."
        
    for b in bookings:
        user = User.query.get(b.user_id)
        trek = Trek.query.get(b.trek_id)
        print(f"[SIMULATED G-CHAT/EMAIL] To: {user.email} -> Reminder: Don't forget your upcoming trek to {trek.name}!")
        
    print("--- REMINDERS SENT ---\n")
    return "Daily Reminders Sent"

@celery.task
def send_monthly_report():
    print("\n--- RUNNING MONTHLY REPORT JOB ---")
    
    total_treks = Trek.query.count()
    total_users = User.query.filter(User.roles.any(name='trekker')).count()
    total_bookings = Booking.query.count()

    html_content = f"""
    <html>
        <head><title>Monthly TMA Report</title></head>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Monthly Trekking Activity Report</h2>
            <hr>
            <p><strong>Total Treks Created:</strong> {total_treks}</p>
            <p><strong>Total Registered Trekkers:</strong> {total_users}</p>
            <p><strong>Total Bookings Processed:</strong> {total_bookings}</p>
            <br>
            <p><em>Generated automatically by Celery</em></p>
        </body>
    </html>
    """
    
    export_dir = os.path.join('static', 'exports')
    filepath = os.path.join(export_dir, 'monthly_admin_report.html')
    
    with open(filepath, 'w') as f:
        f.write(html_content)
    print(f"[SIMULATED EMAIL] Sent to admin@tma.com. Attachment saved at: {filepath}")
    print("--- REPORT GENERATED ---\n")
    return "Monthly Report Generated"
