from flask import Flask
from models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
import uuid

app = Flask(__name__)

# Basic Configuration
app.config['SECRET_KEY'] = 'super-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.sqlite3'
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret-salt-change-this'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

# Initialize DB
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Programmatically create database and admin user
with app.app_context():
    db.create_all() # Creates tables if they don't exist
    
    # Check if roles exist, if not, create them
    if not user_datastore.find_role('admin'):
        user_datastore.create_role(name='admin', description='Administrator')
    if not user_datastore.find_role('staff'):
        user_datastore.create_role(name='staff', description='Trek Staff')
    if not user_datastore.find_role('trekker'):
        user_datastore.create_role(name='trekker', description='General User')
    
    # Check if admin user exists, if not, pre-create it
    if not user_datastore.find_user(email='admin@tma.com'):
        user_datastore.create_user(
            email='admin@tma.com',
            password=hash_password('admin123'),
            roles=['admin'],
            fs_uniquifier=str(uuid.uuid4())
        )
    
    db.session.commit()

@app.route('/')
def home():
    return "Trekking Management API is running!"

if __name__ == '__main__':
    app.run(debug=True)