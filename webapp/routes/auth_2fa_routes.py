"""
Two-Factor Authentication Routes
Add these routes to your auth.py file or import them
"""
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.user import User
import pyotp
import qrcode
import io
import base64

# Add to auth.py after the existing routes:

# ============================================================
# Two-Factor Authentication Routes
# ============================================================

@auth_bp.route('/two-factor-setup', methods=['GET', 'POST'])
@login_required
def two_factor_setup():
    """2FA setup page - generate QR code and enable 2FA"""
    if current_user.two_factor_enabled:
        flash('Two-factor authentication is already enabled', 'info')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        token = request.form.get('token', '').strip()

        if not token:
            flash('Please enter the verification code', 'error')
            return render_template('auth/two-factor-setup.html')

        # Verify the token matches
        if current_user.verify_2fa_token(token):
            # Enable 2FA
            current_user.enable_2fa()
            db.session.commit()

            # Generate and show backup codes
            backup_codes = json.loads(current_user.backup_codes)
            session['show_backup_codes'] = True

            flash('Two-factor authentication has been enabled successfully!', 'success')
            return render_template('auth/backup-codes.html', backup_codes=backup_codes, first_time=True)
        else:
            flash('Invalid verification code. Please try again.', 'error')
            return render_template('auth/two-factor-setup.html')

    # Generate secret if not exists
    if not current_user.two_factor_secret:
        current_user.generate_2fa_secret()
        current_user.generate_backup_codes()
        db.session.commit()

    # Get provisioning URI
    uri = current_user.get_2fa_uri()

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    qr_code = f"data:image/png;base64,{img_str}"

    return render_template('auth/two-factor-setup.html',
                         qr_code=qr_code,
                         secret=current_user.two_factor_secret,
                         email=current_user.email)


@auth_bp.route('/two-step-verification', methods=['GET', 'POST'])
def two_step_verification():
    """2FA verification page during login"""
    # Check if user is in 2FA verification process
    user_id = session.get('2fa_user_id')

    if not user_id:
        flash('Please log in first', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user or not user.two_factor_enabled:
        session.pop('2fa_user_id', None)
        flash('Invalid session', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        use_backup = request.form.get('use_backup') == 'true'

        if not token:
            flash('Please enter a verification code', 'error')
            return render_template('auth/two-step-verification.html', email=user.email)

        # Check if using backup code
        if use_backup:
            if user.verify_backup_code(token):
                db.session.commit()

                # Complete login
                from flask_login import login_user
                login_user(user, remember=session.get('2fa_remember_me', False))
                user.update_last_login()

                # Clear 2FA session
                session.pop('2fa_user_id', None)
                session.pop('2fa_remember_me', None)

                remaining = user.get_remaining_backup_codes()
                if remaining <= 2:
                    flash(f'Login successful! Warning: Only {remaining} backup codes remaining.', 'warning')
                else:
                    flash('Login successful using backup code!', 'success')

                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid backup code', 'error')
                return render_template('auth/two-step-verification.html', email=user.email)
        else:
            # Verify TOTP token
            if user.verify_2fa_token(token):
                # Complete login
                from flask_login import login_user
                login_user(user, remember=session.get('2fa_remember_me', False))
                user.update_last_login()

                # Clear 2FA session
                session.pop('2fa_user_id', None)
                session.pop('2fa_remember_me', None)

                flash(f'Welcome back, {user.full_name or user.username}!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid verification code', 'error')
                return render_template('auth/two-step-verification.html', email=user.email)

    return render_template('auth/two-step-verification.html', email=user.email)


@auth_bp.route('/settings/two-factor', methods=['GET'])
@login_required
def two_factor_settings():
    """2FA settings page"""
    return render_template('auth/two-factor-settings.html',
                         two_factor_enabled=current_user.two_factor_enabled,
                         backup_codes_count=current_user.get_remaining_backup_codes())


@auth_bp.route('/settings/disable-two-factor', methods=['POST'])
@login_required
def disable_two_factor():
    """Disable 2FA"""
    if not current_user.two_factor_enabled:
        return jsonify({'success': False, 'message': '2FA is not enabled'})

    password = request.form.get('password')

    if not password or not current_user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid password'})

    current_user.disable_2fa()
    db.session.commit()

    return jsonify({'success': True, 'message': '2FA has been disabled'})


@auth_bp.route('/settings/regenerate-backup-codes', methods=['POST'])
@login_required
def regenerate_backup_codes():
    """Regenerate backup codes"""
    if not current_user.two_factor_enabled:
        return jsonify({'success': False, 'message': '2FA is not enabled'})

    password = request.form.get('password')

    if not password or not current_user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid password'})

    backup_codes = current_user.generate_backup_codes()
    db.session.commit()

    return jsonify({'success': True, 'backup_codes': backup_codes})


@auth_bp.route('/backup-codes')
@login_required
def view_backup_codes():
    """View backup codes (only right after enabling 2FA)"""
    if not session.get('show_backup_codes'):
        flash('Backup codes are only shown once during setup', 'error')
        return redirect(url_for('auth.two_factor_settings'))

    import json
    backup_codes = json.loads(current_user.backup_codes)
    session.pop('show_backup_codes', None)

    return render_template('auth/backup-codes.html', backup_codes=backup_codes, first_time=True)
