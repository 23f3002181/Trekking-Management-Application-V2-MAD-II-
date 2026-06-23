from flask import Flask
from models import db
from models.user_models import User, Role
from models.trek_models import Trek, Booking
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.staff_routes import staff_bp
from routes.user_routes import user_bp
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)
CSRFProtect(app)

# Basic Configuration
app.config['SECRET_KEY'] = 'super-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.sqlite3'
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret-salt-change-this'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

# API Auth Configs
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['SECURITY_TOKEN_MAX_AGE'] = 3600 
app.config['WTF_CSRF_CHECK_DEFAULT'] = False 
app.config['SECURITY_CSRF_PROTECT_MECHANISMS'] = []
app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False 

# Initialize DB and Security
db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)
# Programmatic Database Initialization
with app.app_context():
    db.create_all()
    
    for role in [('admin', 'Administrator'), ('staff', 'Trek Staff'), ('trekker', 'General User')]:
        if not user_datastore.find_role(role[0]):
            user_datastore.create_role(name=role[0], description=role[1])
            
    if not user_datastore.find_user(email='admin@tma.com'):
        user_datastore.create_user(
            email='admin@tma.com',
            password=hash_password('admin123'),
            roles=['admin'],
            fs_uniquifier=str(uuid.uuid4())
        )
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)