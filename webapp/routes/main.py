from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page - main entry point"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('landing.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - user workspace with tabs"""
    # Redirect to the dashboard blueprint
    return redirect(url_for('dashboard.user_index'))
