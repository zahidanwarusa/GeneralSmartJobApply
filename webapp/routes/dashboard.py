from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models.user import User, JobDescription, Resume, Application
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('admin_auth.login'))

        # Check if user is from Admin table
        from models.admin import Admin
        is_admin = isinstance(current_user._get_current_object(), Admin)

        # Backwards compatibility: check is_admin flag
        if not is_admin and hasattr(current_user, 'is_admin'):
            is_admin = current_user.is_admin

        if not is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('dashboard.user_index'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# USER DASHBOARD ROUTES
# ============================================================================

@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard - redirects based on user type"""
    # Check if logged in user is from Admin table
    from models.admin import Admin
    if isinstance(current_user._get_current_object(), Admin):
        return redirect(url_for('dashboard.admin_index'))
    # Check if user has is_admin flag (backwards compatibility)
    elif hasattr(current_user, 'is_admin') and current_user.is_admin:
        return redirect(url_for('dashboard.admin_index'))
    # Regular user
    return redirect(url_for('dashboard.user_index'))

@dashboard_bp.route('/user')
@login_required
def user_index():
    """User dashboard homepage with tabs"""
    # Get user statistics
    stats = {
        'total_jobs': current_user.job_descriptions.count(),
        'total_resumes': current_user.resumes.count(),
        'total_applications': current_user.applications.count(),
        'active_applications': current_user.applications.filter(
            Application.status.in_(['applied', 'interview'])
        ).count()
    }

    # Get recent applications
    recent_applications = current_user.applications.order_by(
        Application.created_at.desc()
    ).limit(10).all()

    # Get application status breakdown
    status_breakdown = db.session.query(
        Application.status,
        func.count(Application.id)
    ).filter(
        Application.user_id == current_user.id
    ).group_by(Application.status).all()

    return render_template('dashboard/user/index_tabs.html',
                         stats=stats,
                         recent_applications=recent_applications,
                         status_breakdown=dict(status_breakdown))

@dashboard_bp.route('/user/resumes')
@login_required
def user_resumes():
    """User resumes management page"""
    resumes = current_user.resumes.order_by(Resume.created_at.desc()).all()
    return render_template('dashboard/user/resumes.html', resumes=resumes)

@dashboard_bp.route('/user/resume-builder')
@login_required
def user_resume_builder():
    """Resume builder interface"""
    job_id = request.args.get('job_id')
    job = None
    if job_id:
        job = JobDescription.query.filter_by(
            id=job_id,
            user_id=current_user.id
        ).first()

    return render_template('dashboard/user/resume_builder.html', job=job)

@dashboard_bp.route('/user/applications')
@login_required
def user_applications():
    """Application tracking page"""
    applications = current_user.applications.order_by(
        Application.created_at.desc()
    ).all()
    return render_template('dashboard/user/applications.html',
                         applications=applications)

@dashboard_bp.route('/user/applications/kanban')
@login_required
def user_applications_kanban():
    """Kanban board view for applications"""
    applications = current_user.applications.all()

    # Organize applications by status
    kanban_data = {
        'applied': [],
        'interview': [],
        'offer': [],
        'rejected': []
    }

    for app in applications:
        if app.status in kanban_data:
            kanban_data[app.status].append(app)

    return render_template('dashboard/user/kanban.html',
                         kanban_data=kanban_data)

@dashboard_bp.route('/user/jobs')
@login_required
def user_jobs():
    """Job descriptions management"""
    jobs = current_user.job_descriptions.order_by(
        JobDescription.created_at.desc()
    ).all()
    return render_template('dashboard/user/jobs.html', jobs=jobs)

@dashboard_bp.route('/user/analytics')
@login_required
def user_analytics():
    """User statistics and analytics"""
    # Calculate various statistics
    stats = {
        'total_applications': current_user.applications.count(),
        'success_rate': 0,
        'avg_response_time': 0,
        'applications_this_month': 0,
    }

    # Calculate success rate
    total = current_user.applications.count()
    if total > 0:
        successful = current_user.applications.filter(
            Application.status.in_(['interview', 'offer'])
        ).count()
        stats['success_rate'] = (successful / total) * 100

    # Applications this month
    first_day_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    stats['applications_this_month'] = current_user.applications.filter(
        Application.created_at >= first_day_month
    ).count()

    # Get monthly application data for charts
    monthly_data = []
    for i in range(6, 0, -1):
        month_start = (datetime.now() - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        count = current_user.applications.filter(
            Application.created_at >= month_start,
            Application.created_at < month_end
        ).count()
        monthly_data.append({
            'month': month_start.strftime('%b'),
            'count': count
        })

    return render_template('dashboard/user/analytics.html',
                         stats=stats,
                         monthly_data=monthly_data)

@dashboard_bp.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """User profile management"""
    if request.method == 'POST':
        try:
            # Update profile information
            current_user.full_name = request.form.get('full_name', '').strip()

            # Parse date of birth if provided
            dob_str = request.form.get('date_of_birth', '').strip()
            if dob_str:
                try:
                    current_user.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    pass

            current_user.gender = request.form.get('gender', '').strip()
            current_user.country = request.form.get('country', '').strip()
            current_user.language = request.form.get('language', '').strip()

            # Handle profile picture upload
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file and file.filename:
                    # Validate file type
                    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''

                    if file_ext in allowed_extensions:
                        import os
                        from werkzeug.utils import secure_filename
                        from services.supabase_storage import get_storage_service

                        # Generate unique filename
                        filename = f"user_{current_user.id}_{datetime.utcnow().timestamp()}.{file_ext}"
                        filename = secure_filename(filename)

                        # Get MIME type
                        mime_types = {
                            'png': 'image/png',
                            'jpg': 'image/jpeg',
                            'jpeg': 'image/jpeg',
                            'gif': 'image/gif',
                            'webp': 'image/webp'
                        }
                        mimetype = mime_types.get(file_ext, 'image/jpeg')

                        # Try to upload to Supabase Storage first
                        storage_service = get_storage_service()
                        if storage_service.is_available():
                            # Delete old profile picture from Supabase if exists
                            if current_user.profile_picture and 'supabase' in current_user.profile_picture:
                                old_filename = storage_service.get_filename_from_url(current_user.profile_picture)
                                if old_filename:
                                    storage_service.delete_file(old_filename)

                            # Upload to Supabase Storage
                            file_data = file.read()
                            result = storage_service.upload_file(file_data, filename, mimetype)

                            if result['success']:
                                # Store Supabase Storage public URL
                                current_user.profile_picture = result['public_url']
                                flash('Profile picture uploaded successfully!', 'success')
                            else:
                                # Fallback to local storage
                                file.seek(0)  # Reset file pointer
                                upload_folder = os.path.join('webapp', 'static', 'uploads', 'profiles')
                                os.makedirs(upload_folder, exist_ok=True)
                                filepath = os.path.join(upload_folder, filename)
                                file.save(filepath)
                                current_user.profile_picture = f"uploads/profiles/{filename}"
                                flash('Profile picture uploaded locally (Supabase Storage unavailable).', 'warning')
                        else:
                            # Fallback to local storage
                            upload_folder = os.path.join('webapp', 'static', 'uploads', 'profiles')
                            os.makedirs(upload_folder, exist_ok=True)
                            filepath = os.path.join(upload_folder, filename)
                            file.save(filepath)
                            current_user.profile_picture = f"uploads/profiles/{filename}"
                    else:
                        flash('Invalid file type. Please upload an image file (PNG, JPG, JPEG, GIF, WEBP).', 'error')
                        return redirect(url_for('dashboard.user_profile'))

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('dashboard.user_profile'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
            return redirect(url_for('dashboard.user_profile'))

    return render_template('dashboard/user/profile.html')

@dashboard_bp.route('/user/settings')
@login_required
def user_settings():
    """User settings page"""
    return render_template('dashboard/user/settings.html')

# ============================================================================
# ADMIN DASHBOARD ROUTES
# ============================================================================

@dashboard_bp.route('/admin')
@admin_required
def admin_index():
    """Admin dashboard homepage"""
    # System statistics
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'total_applications': Application.query.count(),
        'total_resumes': Resume.query.count(),
        'total_jobs': JobDescription.query.count(),
    }

    # New users this week
    week_ago = datetime.now() - timedelta(days=7)
    stats['new_users_week'] = User.query.filter(
        User.created_at >= week_ago
    ).count()

    # Recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_applications = Application.query.order_by(
        Application.created_at.desc()
    ).limit(10).all()

    # User growth data
    monthly_users = []
    for i in range(6, 0, -1):
        month_start = (datetime.now() - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        count = User.query.filter(
            User.created_at >= month_start,
            User.created_at < month_end
        ).count()
        monthly_users.append({
            'month': month_start.strftime('%b'),
            'count': count
        })

    return render_template('dashboard/admin/index.html',
                         stats=stats,
                         recent_users=recent_users,
                         recent_applications=recent_applications,
                         monthly_users=monthly_users)

@dashboard_bp.route('/admin/users')
@admin_required
def admin_users():
    """User management page"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('dashboard/admin/users.html', users=users)

@dashboard_bp.route('/admin/users/<int:user_id>')
@admin_required
def admin_user_detail(user_id):
    """User detail page"""
    user = User.query.get_or_404(user_id)
    return render_template('dashboard/admin/user_detail.html', user=user)

@dashboard_bp.route('/admin/system-monitor')
@admin_required
def admin_system_monitor():
    """System monitoring page"""
    # Get system metrics
    metrics = {
        'db_size': 'N/A',
        'uptime': 'N/A',
        'api_calls': 'N/A',
        'error_rate': '0.1%'
    }

    # Recent system activity
    recent_activity = []

    # Get latest applications as activity
    applications = Application.query.order_by(
        Application.created_at.desc()
    ).limit(20).all()

    for app in applications:
        recent_activity.append({
            'timestamp': app.created_at,
            'user': app.user.username,
            'action': 'Created application',
            'details': f"Job: {app.job.title if app.job else 'N/A'}"
        })

    return render_template('dashboard/admin/system_monitor.html',
                         metrics=metrics,
                         recent_activity=recent_activity)

@dashboard_bp.route('/admin/payments')
@admin_required
def admin_payments():
    """Payment management page"""
    # Placeholder for future payment integration
    payments = []
    return render_template('dashboard/admin/payments.html', payments=payments)

@dashboard_bp.route('/admin/analytics')
@admin_required
def admin_analytics():
    """System analytics page"""
    # Calculate system-wide analytics
    stats = {
        'total_users': User.query.count(),
        'total_applications': Application.query.count(),
        'total_resumes': Resume.query.count(),
        'avg_applications_per_user': 0
    }

    if stats['total_users'] > 0:
        stats['avg_applications_per_user'] = round(
            stats['total_applications'] / stats['total_users'], 2
        )

    return render_template('dashboard/admin/analytics.html', stats=stats)

# ============================================================================
# PRICING PAGE (AVAILABLE TO ALL LOGGED-IN USERS)
# ============================================================================

@dashboard_bp.route('/pricing')
@login_required
def pricing():
    """Pricing and upgrade plans page"""
    plans = [
        {
            'name': 'Free',
            'price': 0,
            'period': 'forever',
            'features': [
                '5 Resume generations per month',
                'Basic templates',
                '10 Job applications tracking',
                'Email support'
            ],
            'current': True if not hasattr(current_user, 'subscription') else current_user.subscription == 'free'
        },
        {
            'name': 'Pro',
            'price': 19.99,
            'period': 'month',
            'features': [
                'Unlimited resume generations',
                'All premium templates',
                'Unlimited job tracking',
                'Priority support',
                'AI-powered optimization',
                'Export to PDF/DOCX'
            ],
            'recommended': True,
            'current': False
        },
        {
            'name': 'Enterprise',
            'price': 49.99,
            'period': 'month',
            'features': [
                'Everything in Pro',
                'Team collaboration',
                'Custom templates',
                'API access',
                'Dedicated account manager',
                'Advanced analytics'
            ],
            'current': False
        }
    ]

    return render_template('dashboard/pricing.html', plans=plans)

@dashboard_bp.route('/search')
@login_required
def search():
    """Search endpoint for dashboard global search"""
    query = request.args.get('q', '').strip().lower()

    if not query or len(query) < 2:
        return jsonify({'results': []})

    results = []

    # Search user's resumes
    resumes = current_user.resumes.filter(
        Resume.name.ilike(f'%{query}%')
    ).limit(5).all()

    for resume in resumes:
        results.append({
            'id': resume.id,
            'title': resume.name,
            'description': f'Resume - Created {resume.created_at.strftime("%b %d, %Y")}',
            'type': 'resume',
            'url': f'/dashboard/user/resumes'
        })

    # Search user's job descriptions
    jobs = current_user.job_descriptions.filter(
        db.or_(
            JobDescription.title.ilike(f'%{query}%'),
            JobDescription.company.ilike(f'%{query}%')
        )
    ).limit(5).all()

    for job in jobs:
        results.append({
            'id': job.id,
            'title': job.title,
            'description': f'{job.company} - Added {job.created_at.strftime("%b %d, %Y")}',
            'type': 'job',
            'url': f'/dashboard/user/jobs'
        })

    # Search user's applications
    applications = current_user.applications.join(JobDescription).filter(
        db.or_(
            JobDescription.title.ilike(f'%{query}%'),
            JobDescription.company.ilike(f'%{query}%'),
            Application.status.ilike(f'%{query}%')
        )
    ).limit(5).all()

    for app in applications:
        job_title = app.job_description.title if app.job_description else 'Unknown Job'
        company = app.job_description.company if app.job_description else 'Unknown Company'
        results.append({
            'id': app.id,
            'title': f'{job_title} at {company}',
            'description': f'Status: {app.status.title()} - Applied {app.created_at.strftime("%b %d, %Y")}',
            'type': 'application',
            'url': f'/dashboard/user/applications'
        })

    return jsonify({'results': results})

@dashboard_bp.route('/help')
@login_required
def help_faq():
    """Help & FAQ page"""
    faqs = [
        {
            'category': 'Getting Started',
            'questions': [
                {
                    'question': 'How do I create my first resume?',
                    'answer': 'Navigate to "Resume Builder" from the sidebar, fill in your details, and our AI will help you create a professional resume tailored to your target job.'
                },
                {
                    'question': 'Can I import my existing resume?',
                    'answer': 'Yes! You can upload your existing resume in PDF or DOCX format, and our system will parse the information to create an editable version.'
                },
                {
                    'question': 'How do I track my job applications?',
                    'answer': 'Go to "Applications" in the sidebar and click "Add Application" to start tracking your job applications. You can update the status and view them on the Kanban board.'
                }
            ]
        },
        {
            'category': 'Resume Features',
            'questions': [
                {
                    'question': 'Can I create multiple resumes?',
                    'answer': 'Absolutely! You can create unlimited resumes and tailor each one to different job positions or industries.'
                },
                {
                    'question': 'How does the AI optimization work?',
                    'answer': 'Our AI analyzes job descriptions and optimizes your resume content to match keywords and requirements, increasing your chances of passing ATS systems.'
                },
                {
                    'question': 'What formats can I export my resume in?',
                    'answer': 'You can export your resume in PDF and DOCX formats. PDF is recommended for applications, while DOCX allows further editing.'
                }
            ]
        },
        {
            'category': 'Application Tracking',
            'questions': [
                {
                    'question': 'What is the Kanban Board?',
                    'answer': 'The Kanban Board is a visual tool that helps you track your applications through different stages: Applied, Interview, Offer, and Rejected.'
                },
                {
                    'question': 'Can I set reminders for follow-ups?',
                    'answer': 'Yes, you can add notes and set reminders for each application to keep track of follow-up dates and important deadlines.'
                },
                {
                    'question': 'How do I move applications between stages?',
                    'answer': 'Simply drag and drop applications between columns on the Kanban board, or update the status in the application details page.'
                }
            ]
        },
        {
            'category': 'Account & Billing',
            'questions': [
                {
                    'question': 'What\'s included in the free plan?',
                    'answer': 'The free plan includes 5 resume generations per month, basic templates, and tracking up to 10 job applications.'
                },
                {
                    'question': 'How do I upgrade my account?',
                    'answer': 'Click on "Upgrade" in the sidebar to view our premium plans and unlock unlimited resumes, advanced templates, and priority support.'
                },
                {
                    'question': 'Can I cancel my subscription anytime?',
                    'answer': 'Yes, you can cancel your subscription at any time from the Settings page. You\'ll continue to have access until the end of your billing period.'
                }
            ]
        },
        {
            'category': 'Privacy & Security',
            'questions': [
                {
                    'question': 'Is my data secure?',
                    'answer': 'Yes, we use industry-standard encryption to protect your data. Your resumes and personal information are stored securely and never shared with third parties.'
                },
                {
                    'question': 'Can I delete my account?',
                    'answer': 'Yes, you can delete your account from the Settings page. This will permanently remove all your data from our servers.'
                },
                {
                    'question': 'Do you share my information with employers?',
                    'answer': 'No, we never share your information with anyone. You have full control over which resumes you send to employers.'
                }
            ]
        }
    ]

    return render_template('dashboard/help.html', faqs=faqs)
