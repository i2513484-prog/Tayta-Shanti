from flask import Flask
from flask_migrate import Migrate
from app.extensions import db, mail
from app.routes.main import main_bp
from app.routes.admin import admin_bp
from app.extensions import csrf
from app.extensions import limiter


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    mail.init_app(app)

    Migrate(app, db)

    csrf.init_app(app)

    limiter.init_app(app)

    app.register_blueprint(main_bp)

    app.register_blueprint(admin_bp)

    return app