from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse
from extensions import db
from models.user import User
from forms.auth import LoginForm, RegistrationForm
from services.auth_service import AuthService
from services.email_service import EmailService
from datetime import datetime

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
email_service = EmailService()

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

        # Check if email is verified
        if not user.email_verified:
            # Generate new verification code
            code = user.generate_verification_code()
            db.session.commit()

            # Store email in session
            session['pending_verification_email'] = user.email

            # Send verification email
            email_result = email_service.send_verification_code(user.email, code)
            if not email_result['success']:
                print(f"[WARNING] Failed to send email: {email_result['message']}")
                # Still show the code in console as fallback
                print(f"[VERIFICATION CODE] Email: {user.email}, Code: {code}")

            flash('Please verify your email address. A verification code has been sent.', 'warning')
            return redirect(url_for('auth.verify_email'))

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

    from datetime import datetime, date
    now = datetime.now()

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Get additional fields from request
            date_of_birth = request.form.get('date_of_birth')
            gender = request.form.get('gender')
            country = request.form.get('country')
            language = request.form.get('language')

            # Validate required fields
            if not all([date_of_birth, gender, country, language]):
                flash('Please fill in all required fields', 'error')
                return render_template('auth/register.html', form=form, now=now)

            # Validate gender value
            valid_genders = ['male', 'female', 'other', 'prefer_not_to_say']
            if gender not in valid_genders:
                flash('Invalid gender selection', 'error')
                return render_template('auth/register.html', form=form, now=now)

            # Parse and validate date of birth
            try:
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

                # Check if user is at least 13 years old
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 13:
                    flash('You must be at least 13 years old to register', 'error')
                    return render_template('auth/register.html', form=form, now=now)

                # Check if date is not in the future
                if dob > today:
                    flash('Date of birth cannot be in the future', 'error')
                    return render_template('auth/register.html', form=form, now=now)

            except (ValueError, TypeError):
                flash('Invalid date format. Please use a valid date.', 'error')
                return render_template('auth/register.html', form=form, now=now)

            # Validate country
            if not country or len(country) > 100:
                flash('Invalid country selection', 'error')
                return render_template('auth/register.html', form=form, now=now)

            # Validate language
            if not language or len(language) > 50:
                flash('Invalid language selection', 'error')
                return render_template('auth/register.html', form=form, now=now)

            # Create new user
            user = User(
                email=form.email.data.lower().strip(),
                username=form.username.data.lower().strip(),
                full_name=form.full_name.data.strip(),
                date_of_birth=dob,
                gender=gender,
                country=country,
                language=language,
                profile_completed=True
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            # Generate and send verification code
            code = user.generate_verification_code()
            db.session.commit()

            # Store email in session for verification
            session['pending_verification_email'] = user.email

            # Send verification email
            email_result = email_service.send_verification_code(user.email, code)
            if not email_result['success']:
                print(f"[WARNING] Failed to send email: {email_result['message']}")
                # Still show the code in console as fallback
                print(f"[VERIFICATION CODE] Email: {user.email}, Code: {code}")

            flash('Registration successful! Please check your email for the verification code.', 'success')
            return redirect(url_for('auth.verify_email'))

        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('auth/register.html', form=form, now=now)

    return render_template('auth/register.html', form=form, now=now)

@auth_bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    # Clear all flash messages
    session.pop('_flashes', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/complete-signup', methods=['GET', 'POST'])
def complete_signup():
    """Complete OAuth signup with additional user information"""
    # Check if we have OAuth signup data
    oauth_data = session.get('oauth_signup_data')
    if not oauth_data:
        flash('Invalid signup session. Please try again.', 'error')
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        from datetime import datetime, date
        now = datetime.now()

        try:
            # Get form data
            username = request.form.get('username', '').strip()
            full_name = request.form.get('full_name', '').strip()
            date_of_birth = request.form.get('date_of_birth')
            gender = request.form.get('gender')
            country = request.form.get('country')
            language = request.form.get('language')
            email = oauth_data['email']

            # Validate required fields
            if not all([username, full_name, date_of_birth, gender, country, language]):
                flash('Please fill in all required fields', 'error')
                return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            # Validate username length and format
            if len(username) < 3 or len(username) > 80:
                flash('Username must be between 3 and 80 characters', 'error')
                return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            # Check if username is already taken
            existing_user = User.query.filter_by(username=username.lower()).first()
            if existing_user:
                flash('Username already taken. Please choose another.', 'error')
                return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            # Validate full name length
            if len(full_name) < 2 or len(full_name) > 120:
                flash('Full name must be between 2 and 120 characters', 'error')
                return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            # Validate gender value
            valid_genders = ['male', 'female', 'other', 'prefer_not_to_say']
            if gender not in valid_genders:
                flash('Invalid gender selection', 'error')
                return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            # Parse and validate date of birth
            try:
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

                # Check if user is at least 13 years old
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 13:
                    flash('You must be at least 13 years old to register', 'error')
                    return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

                # Check if date is not in the future
                if dob > today:
                    flash('Date of birth cannot be in the future', 'error')
                    return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            except (ValueError, TypeError):
                flash('Invalid date format. Please use a valid date.', 'error')
                return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            # Validate country
            if not country or len(country) > 100:
                flash('Invalid country selection', 'error')
                return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            # Validate language
            if not language or len(language) > 50:
                flash('Invalid language selection', 'error')
                return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=now)

            # Create user
            user = User(
                supabase_user_id=oauth_data['supabase_user_id'],
                email=email.lower().strip(),
                username=username.lower(),
                full_name=full_name,
                date_of_birth=dob,
                gender=gender,
                country=country,
                language=language,
                profile_completed=True,
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

        except Exception as e:
            db.session.rollback()
            print(f"OAuth signup completion error: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=datetime.now())

    # GET request - show form
    from datetime import datetime
    return render_template('auth/complete_signup.html', oauth_data=oauth_data, now=datetime.now())

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

        # Check if user exists in database
        user = User.query.filter_by(email=user_data.email).first()

        if not user:
            # New user - redirect to complete signup form
            metadata = user_data.user_metadata or {}

            # Store OAuth data in session for registration form
            session['oauth_signup_data'] = {
                'supabase_user_id': user_data.id,
                'email': user_data.email,
                'full_name': metadata.get('full_name') or metadata.get('name', ''),
                'picture': metadata.get('picture') or metadata.get('avatar_url', ''),
                'provider': 'google'
            }

            # Store Supabase tokens
            supabase_session = result['session']
            session['access_token'] = supabase_session.access_token
            session['refresh_token'] = supabase_session.refresh_token

            return redirect(url_for('auth.complete_signup'))
        else:
            # Existing user - log in directly
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

            flash(f'Welcome back, {user.full_name or user.username}!', 'success')
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


@auth_bp.route('/email-verification', methods=['GET', 'POST'])
def verify_email():
    """Email verification page"""
    email = session.get('pending_verification_email')
    
    if not email:
        flash('No pending verification. Please register or log in.', 'error')
        return redirect(url_for('auth.register'))
    
    if request.method == 'POST':
        verification_code = request.form.get('verification_code', '').strip()
        
        if not verification_code or len(verification_code) != 6:
            flash('Please enter a valid 6-digit code', 'error')
            return render_template('auth/email_verification.html', email=email)
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('auth.register'))
        
        if user.verify_code(verification_code):
            user.email_verified = True
            user.verification_code = None
            user.verification_code_expires = None
            db.session.commit()
            
            # Clear session
            session.pop('pending_verification_email', None)
            
            # Log in the user
            login_user(user, remember=True)
            user.update_last_login()
            
            flash('Email verified successfully! Welcome to SmartApply Pro.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid or expired verification code', 'error')
            return render_template('auth/email_verification.html', email=email)
    
    return render_template('auth/email_verification.html', email=email)

@auth_bp.route('/resend-verification-code', methods=['POST'])
def resend_verification_code():
    """Resend verification code"""
    email = session.get('pending_verification_email')

    if not email:
        return jsonify({'success': False, 'message': 'No pending verification'})

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    # Generate new code
    code = user.generate_verification_code()
    db.session.commit()

    # Send verification email
    email_result = email_service.send_verification_code(user.email, code)
    if not email_result['success']:
        print(f"[WARNING] Failed to send email: {email_result['message']}")
        # Still show the code in console as fallback
        print(f"[VERIFICATION CODE RESENT] Email: {user.email}, Code: {code}")

    return jsonify({'success': True, 'message': 'Verification code resent'})
