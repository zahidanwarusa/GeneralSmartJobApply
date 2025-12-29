# SmartApply Pro - Web Application

AI-Powered Resume Optimization Platform with Clean Black & White Design

## Quick Start

### 1. Install Dependencies

```bash
cd webapp
pip install -r requirements.txt
```

### 2. Setup Environment

Copy the example environment file and configure it:

```bash
copy .env.example .env
```

Edit `.env` and set your configuration (or leave defaults for development).

### 3. Initialize Database

```bash
python init_db.py
```

This will create the SQLite database and optionally create a test user.

### 4. Run the Application

```bash
python app.py
```

The application will be available at: http://localhost:5000

### 5. Access the App

- **Landing Page**: http://localhost:5000
- **Login**: http://localhost:5000/auth/login
- **Register**: http://localhost:5000/auth/register

**Test User** (if created):
- Email: `test@example.com`
- Password: `password123`

## Project Structure

```
webapp/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── extensions.py          # Flask extensions
├── requirements.txt       # Python dependencies
├── init_db.py            # Database initialization script
│
├── models/               # Database models
│   ├── __init__.py
│   └── user.py          # User, JobDescription, Resume, Application models
│
├── routes/              # Application routes (blueprints)
│   ├── auth.py         # Authentication routes
│   └── main.py         # Main app routes
│
├── forms/               # WTForms form classes
│   ├── __init__.py
│   └── auth.py         # Login and registration forms
│
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Landing page
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── dashboard/
│       └── index.html  # Dashboard (Week 3)
│
└── static/             # Static files
    ├── css/
    │   └── style.css  # Black & white design
    ├── js/
    └── img/
```

## Features Completed (Week 1)

✅ User registration with validation
✅ User login with session management
✅ Clean black & white UI design
✅ SQLite database with SQLAlchemy ORM
✅ Password hashing (bcrypt)
✅ Form validation
✅ Flash messages
✅ Responsive design

## Next Steps (Week 2-6)

- Week 2: Job description & resume generation API
- Week 3: Dashboard UI with Bootstrap
- Week 4: Multi-user features & templates
- Week 5: Background jobs & cloud deployment
- Week 6: Security, testing & launch

## Development Commands

**Initialize database:**
```bash
python init_db.py
```

**Run development server:**
```bash
python app.py
```

**Flask shell (for testing):**
```bash
flask shell
```

## Database Models

- **User**: User accounts and authentication
- **JobDescription**: Uploaded job descriptions
- **Resume**: Generated resumes
- **Application**: Application tracking

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: SQLite (dev) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF + WTForms
- **Frontend**: HTML5 + CSS3 (minimal JavaScript)
- **Design**: Custom black & white minimalist theme

## Notes

- Currently using SQLite for development (file-based database)
- Will migrate to PostgreSQL for production deployment
- Session management with secure cookies
- Password hashing using bcrypt
- CSRF protection enabled on all forms
