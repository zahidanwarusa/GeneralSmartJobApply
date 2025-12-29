from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse
from extensions import db
from models.user import User
from forms.auth import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Your account has been deactivated. Please contact support.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        user.update_last_login()

        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.dashboard')

        flash(f'Welcome back, {user.full_name or user.username}!', 'success')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            username=form.username.data.lower(),
            full_name=form.full_name.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page - sends reset email"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email.lower()).first()

        # Always show success message for security (don't reveal if email exists)
        flash('If an account exists with this email, you will receive password reset instructions.', 'success')

        if user:
            # TODO: Implement email sending with reset token
            # For now, just log it
            print(f"Password reset requested for: {email}")

        return redirect(url_for('auth.login'))

    return render_template('auth/forgot-password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page - validates token and resets password"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # TODO: Validate token and get user
    # For now, just render the template

    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.reset_password', token=token))

        # TODO: Update user password
        flash('Your password has been reset successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset-password.html', token=token)

@auth_bp.route('/email-verification')
def email_verification():
    """Email verification page"""
    email = request.args.get('email', 'your email')
    return render_template('auth/email-verification.html', email=email)

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """Process email verification"""
    # TODO: Implement email verification logic
    flash('Email verified successfully!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/resend-verification')
def resend_verification():
    """Resend verification email"""
    # TODO: Implement resend verification email
    flash('Verification email has been resent.', 'info')
    return redirect(url_for('auth.email_verification'))

@auth_bp.route('/two-step-verification')
def two_step_verification():
    """Two-step verification page"""
    email = request.args.get('email', 'your email')
    return render_template('auth/two-step.html', email=email)

@auth_bp.route('/verify-two-step', methods=['POST'])
def verify_two_step():
    """Process two-step verification code"""
    digit1 = request.form.get('digit1')
    digit2 = request.form.get('digit2')
    digit3 = request.form.get('digit3')
    digit4 = request.form.get('digit4')

    code = f"{digit1}{digit2}{digit3}{digit4}"

    # TODO: Validate the code
    if code == "1234":  # Placeholder validation
        flash('Verification successful!', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Invalid verification code', 'error')
        return redirect(url_for('auth.two_step_verification'))

@auth_bp.route('/resend-code')
def resend_code():
    """Resend two-step verification code"""
    # TODO: Implement resend code logic
    flash('Verification code has been resent.', 'info')
    return redirect(url_for('auth.two_step_verification'))
