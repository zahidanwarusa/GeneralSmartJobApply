"""
Admin authentication routes - separate login for admins
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from extensions import db
from models.admin import Admin

admin_auth_bp = Blueprint('admin_auth', __name__, url_prefix='/admin')


@admin_auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if current_user.is_authenticated and hasattr(current_user, 'is_admin') and current_user.is_admin:
        return redirect(url_for('dashboard.admin_index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        admin = Admin.query.filter_by(email=email.lower()).first()

        if admin is None or not admin.check_password(password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('admin_auth.login'))

        if not admin.is_active:
            flash('Your admin account has been deactivated.', 'error')
            return redirect(url_for('admin_auth.login'))

        # Login with admin_ prefix
        login_user(admin, remember=remember)
        # Override get_id to return prefixed ID
        admin.get_id = lambda: f"admin_{admin.id}"

        admin.update_last_login()

        flash(f'Welcome back, {admin.full_name or admin.username}!', 'success')
        return redirect(url_for('dashboard.admin_index'))

    return render_template('auth/admin_login.html')


@admin_auth_bp.route('/logout')
def logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('admin_auth.login'))
