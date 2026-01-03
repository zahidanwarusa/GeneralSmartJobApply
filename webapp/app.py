from flask import Flask, redirect, url_for, render_template
from config import config
from extensions import db, login_manager, migrate
from models.user import User
from sqlalchemy.exc import OperationalError, DBAPIError
import logging

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return "404 - Page Not Found", 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return "500 - Internal Server Error", 500

    @app.errorhandler(OperationalError)
    def handle_db_operational_error(error):
        """Handle database operational errors"""
        db.session.rollback()
        logging.error(f"Database operational error: {str(error)}")
        return "Database connection error. Please try again in a moment.", 503

    @app.errorhandler(DBAPIError)
    def handle_db_api_error(error):
        """Handle database API errors"""
        db.session.rollback()
        logging.error(f"Database API error: {str(error)}")
        return "Database error. Please try again in a moment.", 503

    # Shell context for flask shell
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User
        }

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
