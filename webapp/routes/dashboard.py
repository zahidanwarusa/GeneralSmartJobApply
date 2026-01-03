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

@dashboard_bp.route('/user/profile')
@login_required
def user_profile():
    """User profile management"""
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
