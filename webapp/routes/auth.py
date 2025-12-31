from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse
from extensions import db
from models.user import User
from forms.auth import LoginForm, RegistrationForm
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

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

@auth_bp.route('/complete-signup', methods=['GET', 'POST'])
def complete_signup():
    """Complete OAuth signup with additional user information"""
    # Check if we have OAuth signup data
    oauth_data = session.get('oauth_signup_data')
    if not oauth_data:
        flash('Invalid signup session. Please try again.', 'error')
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        email = oauth_data['email']

        # Validate required fields
        if not username or not full_name:
            flash('Please fill in all required fields', 'error')
            return render_template('auth/complete_signup.html', oauth_data=oauth_data)

        # Check if username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose another.', 'error')
            return render_template('auth/complete_signup.html', oauth_data=oauth_data)

        # Create user
        user = User(
            supabase_user_id=oauth_data['supabase_user_id'],
            email=email,
            username=username,
            full_name=full_name,
            is_active=True,
            password_hash=None  # OAuth users don't need password
        )
        db.session.add(user)
        db.session.commit()

        # Log in the user
        login_user(user, remember=True)
        user.update_last_login()

        # Store Supabase tokens in session
        session['supabase_user_id'] = oauth_data['supabase_user_id']
        # access_token and refresh_token are already in session from OAuth flow

        # Clear OAuth signup data
        session.pop('oauth_signup_data', None)
        session.pop('oauth_flow', None)

        flash(f'Welcome to SmartApply Pro, {user.full_name}!', 'success')
        return redirect(url_for('main.dashboard'))

    # GET request - show form
    return render_template('auth/complete_signup.html', oauth_data=oauth_data)

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

# Supabase OAuth Routes
@auth_bp.route('/oauth/signup/<provider>')
def oauth_signup(provider):
    """
    Initiate OAuth SIGNUP with specified provider (creates new account)
    Supported providers: google, github, microsoft, apple, discord, etc.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Store that this is a signup flow
    session['oauth_flow'] = 'signup'

    # Get the redirect URL
    redirect_to = url_for('auth.oauth_callback', _external=True)

    # Initiate OAuth flow
    result = auth_service.sign_in_with_oauth(provider, redirect_to)

    if result['success']:
        # Redirect to OAuth provider
        return redirect(result['url'])
    else:
        flash(result['message'], 'error')
        return redirect(url_for('auth.register'))

@auth_bp.route('/oauth/login/<provider>')
def oauth_login(provider):
    """
    Initiate OAuth LOGIN with specified provider (existing account only)
    Supported providers: google, github, microsoft, apple, discord, etc.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Store that this is a login flow
    session['oauth_flow'] = 'login'

    # Get the redirect URL
    redirect_to = url_for('auth.oauth_callback', _external=True)

    # Initiate OAuth flow
    result = auth_service.sign_in_with_oauth(provider, redirect_to)

    if result['success']:
        # Redirect to OAuth provider
        return redirect(result['url'])
    else:
        flash(result['message'], 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/callback')
def oauth_callback():
    """
    OAuth callback handler
    Exchanges authorization code for session
    """
    # Get the authorization code from URL parameters
    code = request.args.get('code')
    error = request.args.get('error')

    if error:
        flash(f'Authentication error: {error}', 'error')
        return redirect(url_for('auth.login'))

    if not code:
        flash('No authorization code received', 'error')
        return redirect(url_for('auth.login'))

    # Exchange code for session
    result = auth_service.exchange_code_for_session(code)

    if result['success']:
        user_data = result['user']

        # Check if user exists in database, if not create them
        user = User.query.filter_by(email=user_data.email).first()

        if not user:
            # Create new user from OAuth data
            user = User(
                supabase_user_id=user_data.id,
                email=user_data.email,
                username=user_data.email.split('@')[0],  # Generate username from email
                full_name=user_data.user_metadata.get('full_name', ''),
                is_active=True
            )
            # OAuth users don't need password
            user.password_hash = None
            db.session.add(user)
            db.session.commit()
        else:
            # Update supabase_user_id if not set
            if not user.supabase_user_id:
                user.supabase_user_id = user_data.id
                db.session.commit()

        # Log in the user
        login_user(user, remember=True)
        user.update_last_login()

        # Store Supabase session data in Flask session (convert to dict for JSON serialization)
        supabase_session = result['session']
        session['supabase_access_token'] = supabase_session.access_token
        session['supabase_refresh_token'] = supabase_session.refresh_token
        session['supabase_user_id'] = user_data.id

        flash(f'Welcome, {user.full_name or user.username}!', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash(result['message'], 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/supabase/register', methods=['POST'])
def supabase_register():
    """
    Register user with Supabase (Email/Password)
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name', '')

    result = auth_service.sign_up_with_email(
        email=email,
        password=password,
        user_metadata={'full_name': full_name}
    )

    if result['success']:
        flash(result['message'], 'success')
        return redirect(url_for('auth.login'))
    else:
        flash(result['message'], 'error')
        return redirect(url_for('auth.register'))

@auth_bp.route('/supabase/login', methods=['POST'])
def supabase_login():
    """
    Login user with Supabase (Email/Password)
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    email = request.form.get('email')
    password = request.form.get('password')

    result = auth_service.sign_in_with_email(email, password)

    if result['success']:
        user_data = result['user']

        # Check if user exists in database
        user = User.query.filter_by(email=user_data.email).first()

        if not user:
            # Create new user
            user = User(
                supabase_user_id=user_data.id,
                email=user_data.email,
                username=user_data.email.split('@')[0],
                full_name=user_data.user_metadata.get('full_name', ''),
                is_active=True
            )
            db.session.add(user)
            db.session.commit()
        else:
            # Update supabase_user_id if not set
            if not user.supabase_user_id:
                user.supabase_user_id = user_data.id
                db.session.commit()

        # Log in the user
        login_user(user, remember=True)
        user.update_last_login()

        # Store Supabase session data in Flask session (convert to dict for JSON serialization)
        supabase_session = result['session']
        session['supabase_access_token'] = supabase_session.access_token
        session['supabase_refresh_token'] = supabase_session.refresh_token
        session['supabase_user_id'] = user_data.id

        flash(result['message'], 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash(result['message'], 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/supabase/session', methods=['POST'])
def supabase_session():
    """
    Handle Supabase OAuth session tokens from frontend
    """
    from flask import jsonify
    import traceback

    print("[DEBUG] ========== OAuth Session Handler Called ==========")

    data = request.get_json()
    print(f"[DEBUG] Received data keys: {list(data.keys()) if data else 'None'}")

    if not data or 'access_token' not in data:
        print("[ERROR] No access token in request data")
        return jsonify({'success': False, 'message': 'Invalid session data - no access token'})

    try:
        # Use Supabase client to get user info from access token
        from supabase_client import get_supabase_client
        print("[DEBUG] Getting Supabase client...")
        supabase = get_supabase_client()

        # Set the session in Supabase client
        print("[DEBUG] Setting session in Supabase client...")
        supabase.auth.set_session(data['access_token'], data.get('refresh_token', ''))

        # Get user info
        print("[DEBUG] Getting user info from access token...")
        user_response = supabase.auth.get_user(data['access_token'])

        if not user_response or not user_response.user:
            print("[ERROR] Could not get user info from Supabase")
            return jsonify({'success': False, 'message': 'Could not get user info from Supabase'})

        user_data = user_response.user
        email = user_data.email
        print(f"[DEBUG] User email from Supabase: {email}")

        if not email:
            print("[ERROR] No email in Supabase user data")
            return jsonify({'success': False, 'message': 'No email in session'})

        # Check if user exists in local database
        print(f"[DEBUG] Checking if user exists in local database: {email}")
        user = User.query.filter_by(email=email).first()

        # Get OAuth flow type (signup or login)
        oauth_flow = session.get('oauth_flow', 'login')
        print(f"[DEBUG] OAuth flow type: {oauth_flow}")

        if not user:
            # User doesn't exist
            if oauth_flow == 'login':
                # Login flow but user doesn't exist - ERROR
                print(f"[ERROR] Login attempted but user doesn't exist: {email}")
                return jsonify({
                    'success': False,
                    'message': 'No account found. Please sign up first.',
                    'redirect': '/auth/register'
                })

            # Signup flow - store OAuth data in session and redirect to registration form
            print(f"[DEBUG] OAuth signup - storing data in session for registration form")
            metadata = user_data.user_metadata or {}

            # Store OAuth data in session for registration form
            session['oauth_signup_data'] = {
                'supabase_user_id': user_data.id,
                'email': email,
                'full_name': metadata.get('full_name') or metadata.get('name', ''),
                'picture': metadata.get('picture') or metadata.get('avatar_url', ''),
                'provider': 'google'  # Can be dynamic based on provider
            }
            session['access_token'] = data.get('access_token')
            session['refresh_token'] = data.get('refresh_token')

            print(f"[DEBUG] Redirecting to registration form to complete signup")
            return jsonify({
                'success': True,
                'message': 'Please complete your registration',
                'redirect': '/auth/complete-signup',
                'requires_form': True
            })
        else:
            # User exists
            if oauth_flow == 'signup':
                # Signup flow but user already exists - ERROR
                print(f"[ERROR] Signup attempted but user already exists: {email}")
                return jsonify({
                    'success': False,
                    'message': 'Account already exists. Please sign in instead.',
                    'redirect': '/auth/login'
                })

            # Login flow with existing user - OK
            print(f"[DEBUG] Existing user logging in with ID: {user.id}")
            # Update supabase_user_id if not set
            if not user.supabase_user_id:
                user.supabase_user_id = user_data.id
                db.session.commit()
                print(f"[DEBUG] Updated user with Supabase ID: {user.supabase_user_id}")

        # Clear OAuth flow from session
        session.pop('oauth_flow', None)

        # Log in the user with Flask-Login
        print("[DEBUG] Logging in user with Flask-Login...")
        login_user(user, remember=True)
        user.update_last_login()
        print(f"[DEBUG] User logged in. is_authenticated: {current_user.is_authenticated}")

        # Store Supabase tokens in session
        session['access_token'] = data.get('access_token')
        session['refresh_token'] = data.get('refresh_token')
        session['supabase_user_id'] = user_data.id
        print("[DEBUG] Supabase tokens stored in Flask session")

        print("[DEBUG] ========== OAuth Login Successful ==========")
        return jsonify({
            'success': True,
            'message': 'Logged in successfully',
            'user': {
                'email': user.email,
                'full_name': user.full_name
            }
        })

    except Exception as e:
        print(f"[ERROR] ========== OAuth session error ==========")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        print(f"[ERROR] Error message: {str(e)}")
        print(f"[ERROR] Traceback:")
        traceback.print_exc()
        print(f"[ERROR] ==========================================")
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'})
