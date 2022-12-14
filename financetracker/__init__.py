from os import path

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME = 'database.db'
migrate = Migrate()

UPLOAD_FOLDER = 'C:\\Users\\fenik\\Documents\\GitHub\\Finance Tracker\\financetracker\\static\\uploads'
ALLOWED_EXTENSIONS = {'xls'}


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'zHyouxw7ztlfgkUV6RfLYY4pifWvT8CD'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://eayogxfttccwxt:6bb4cf7b09de2cefec44377a68aaadc2def71b9cb1036f6aa1213edafd1e9da9@ec2-54-228-32-29.eu-west-1.compute.amazonaws.com:5432/d7l426kqhamgvq'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/')
    def home():
        return redirect(url_for('views.home'))

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    migrate.init_app(app, db)

    return app


def create_database(app):
    if not path.exists('financetracker/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
