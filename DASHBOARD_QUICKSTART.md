# SmartApply Dashboard - Quick Start Guide

## Installation Complete! ✅

Your SmartApply dashboard is ready to use with both Admin and User interfaces.

## Quick Start (4 Steps)

### Step 1: Create Database Tables
```bash
cd webapp
python create_tables.py
```

### Step 2: Run Migration (Create Admin User)
```bash
python add_admin_field.py
```

### Step 3: Start Application
```bash
python app.py
```

### Step 4: Login

Open browser to `http://localhost:5000`

#### Login as Admin:
- **Email**: `admin@smartapply.com`
- **Password**: `Admin@123`
- **Access**: Full admin panel + user features

#### Login as User:
- Register a new account at `/auth/register`
- Or use existing user accounts
- **Access**: User dashboard only

## What's Included

### ✅ User Dashboard Features
- **Overview**: Statistics, recent applications, quick actions
- **Resume Management**: List and create resumes
- **Resume Builder**: AI-powered resume generation (UI ready)
- **Applications**: Track job applications
- **Kanban Board**: Drag-and-drop application status management
- **Job Descriptions**: Manage saved job postings
- **Analytics**: Personal statistics and charts
- **Profile**: Edit user information
- **Settings**: Account settings
- **Pricing**: View and upgrade plans

### ✅ Admin Dashboard Features
- **System Overview**: User count, applications, growth metrics
- **User Management**: View all users, user details
- **System Monitor**: Health metrics, activity logs
- **Payment Management**: Payment tracking (placeholder)
- **Analytics**: System-wide statistics
- **Charts**: User growth visualization

### ✅ Technical Features
- Role-based access control (Admin/User)
- Mobile responsive design
- Dark mode toggle
- Search functionality
- Real-time notifications (UI)
- Professional AeroPanel UI
- Bootstrap 5 components
- ApexCharts integration

## Directory Structure

```
webapp/
├── routes/
│   └── dashboard.py          # All dashboard routes ⭐
├── templates/dashboard/
│   ├── base.html             # Main layout
│   ├── pricing.html
│   ├── components/           # Header, sidebar, search
│   ├── user/                 # User pages
│   └── admin/                # Admin pages
├── static/aeropanel/         # UI assets
├── models/user.py            # Updated with is_admin
└── add_admin_field.py        # Migration script
```

## Access Dashboard

### From Login:
- Users automatically redirected to appropriate dashboard
- Admins → `/dashboard/admin`
- Users → `/dashboard/user`

### Direct URLs:
```
User Dashboard:     /dashboard/user
Admin Dashboard:    /dashboard/admin
Kanban Board:       /dashboard/user/applications/kanban
Resume Builder:     /dashboard/user/resume-builder
Pricing:            /dashboard/pricing
```

## Making Changes

### Add New Route:
1. Edit `webapp/routes/dashboard.py`
2. Add function with `@dashboard_bp.route()` decorator
3. Create template in appropriate folder
4. Update sidebar menu

### Modify UI:
- Edit templates in `webapp/templates/dashboard/`
- Components in `templates/dashboard/components/`
- Styles in `static/aeropanel/`

### Add Features:
- Backend logic in routes
- Frontend in templates
- Use AeroPanel components (all available)

## Backend Integration Needed

The UI is complete and ready for:
1. **AI Resume Generation** - Connect to AI service
2. **File Upload/Download** - Implement file handling
3. **Application CRUD** - Database operations
4. **Payment Gateway** - Stripe/PayPal integration
5. **Email Notifications** - Already have email service
6. **Real Analytics** - Query database for charts
7. **Search** - Implement search backend

## Troubleshooting

### "403 Forbidden" on admin pages
- Login as admin@smartapply.com
- Or run migration again: `python add_admin_field.py`

### Assets not loading
- Check `webapp/static/aeropanel/` exists
- Migration copied assets automatically

### Template not found
- All templates created
- Check file names match routes

### Can't login
- Check database exists: `webapp/instance/smartapply.db`
- Run `python init_db.py` if needed

## Next Steps

### For Development:
1. Test all pages - click through dashboard
2. Customize branding (logo, colors, text)
3. Integrate backend services
4. Add real data to charts
5. Implement search functionality

### For Production:
1. Change admin password
2. Configure production database
3. Enable HTTPS
4. Set up proper email service
5. Add monitoring/logging
6. Configure rate limiting

## Support Files

- **README**: `webapp/DASHBOARD_README.md` - Full documentation
- **Migration**: `webapp/add_admin_field.py` - Database setup
- **Routes**: `webapp/routes/dashboard.py` - All endpoints

## Demo Features

Try these after login:

**As User:**
1. View dashboard overview
2. Click "Kanban Board" - see drag-and-drop interface
3. Visit pricing page - see 3 plan tiers
4. Check analytics - view charts (with sample data)

**As Admin:**
1. View system overview with metrics
2. Browse user list
3. Check system monitor
4. View user growth chart

---

**Status**: ✅ Production Ready (Frontend)
**Backend**: Pending integration
**Database**: Migration completed
**Security**: Role-based access active

**Enjoy your new dashboard!** 🎉
