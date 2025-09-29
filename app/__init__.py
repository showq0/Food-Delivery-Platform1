from flask import Flask
from .extensions import db, jwt, bcrypt
from feature1.routes import user_bp
from feature2.routes import order_bp
from feature3.routes import loc_bp
from feature5.routes import chat_bp
from feature4.routes import notific_bp
from feature6.routes import announcement_bp
from feature7.routes import image_pros_bp
from .extensions import socketio
# models need to be imported here for creating tables
from feature1.models import User
from feature2.models import Order
from feature4.models import Restaurant
from feature5.models import Chat, Message
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'

    # Initialize database
    db.init_app(app)
    # to handle WebSocket connections alongside normal HTTP requests.
    socketio.init_app(app, cors_allowed_origins="*")

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_TOKEN_LOCATION"] = [os.getenv('JWT_TOKEN_LOCATION')]
    app.config["JWT_COOKIE_SECURE"] = os.getenv('JWT_COOKIE_SECURE') == 'False'
    app.config["JWT_COOKIE_CSRF_PROTECT"] = os.getenv('JWT_COOKIE_CSRF_PROTECT') == 'False'
    # for JWT and hashing
    jwt.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    app.register_blueprint(user_bp, url_prefix='/')
    app.register_blueprint(order_bp, url_prefix='/order')
    app.register_blueprint(loc_bp, url_prefix='/location')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(notific_bp, url_prefix='/notification')
    app.register_blueprint(announcement_bp, url_prefix='/announcement')
    app.register_blueprint(image_pros_bp, url_prefix='/image_pros')

    with app.app_context():
        db.create_all()
    return app
