from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql  # Assure-toi d'avoir installé PyMySQL 
from flask_migrate import Migrate 

db = SQLAlchemy()
migrate = Migrate() 

# Configuration de la base de données MySQL
DB_USER = "root"          # Ton utilisateur MySQL
DB_PASSWORD = ""  # Ton mot de passe MySQL
DB_HOST = "localhost"     # Adresse du serveur MySQL (localhost si en local)
DB_NAME = "ecommerce"  # Nom de la base de données



def create_database():
    db.create_all()
    print('Database Created')


def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

    db.init_app(app)
    migrate.init_app(app, db)  # Initialise Flask-Migrate

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .app_views  import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Cart, Product, Order

    app.register_blueprint(views, url_prefix='/') # localhost:5000/about-us
    app.register_blueprint(auth, url_prefix='/') # localhost:5000/auth/change-password
    app.register_blueprint(admin, url_prefix='/')

    # with app.app_context():
    #     create_database()

    return app

