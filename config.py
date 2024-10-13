from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from redis_utils.redis_manager import RedisConnectionHandler
from redis_utils.redis_methods import RedisMethodsHandler


db = SQLAlchemy()

redis_connection = RedisConnectionHandler(f'localhost', 6379, 0).make_connection()
redis_methods_connection = RedisMethodsHandler(redis_connection)

def create_app():

    load_dotenv()
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    db.init_app(app)
    
    from models.db_models import User, Transactions
    
    with app.app_context():
        db.create_all()
        
    
    from controllers.home_controller import home_controller
    from controllers.views import views_controller
    from controllers.registration_controller import registrations_controller
    from controllers.pix_keys_controller import pix_keys_controller
    from controllers.pix_controller import pix_controller
    app.register_blueprint(home_controller)
    app.register_blueprint(views_controller)
    app.register_blueprint(registrations_controller)
    app.register_blueprint(pix_keys_controller)
    app.register_blueprint(pix_controller)
    return app