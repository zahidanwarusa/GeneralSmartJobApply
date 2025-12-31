from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main index - handles OAuth callback with hash fragments"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # This page will detect OAuth tokens in hash and process them
    # or redirect to landing page if no tokens
    return render_template('auth/oauth_handler.html')

@main_bp.route('/landing')
def landing():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('landing.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - will be built in Week 3"""
    return render_template('dashboard/index.html')
