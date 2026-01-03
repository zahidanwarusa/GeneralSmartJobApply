# Dashboard Quick Start Guide

## Starting the Application

1. **Navigate to webapp directory:**
   ```bash
   cd "C:\Users\ABC\OneDrive\Desktop\Testing and Modification\GeneralSmartJobApply\GeneralSmartApplyPro\webapp"
   ```

2. **Start the Flask application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   - Open browser and go to: `http://localhost:5000`

## First Time Setup

### 1. Create an Account
- Click "Sign Up" or "Register"
- Fill in your details (email, password, full name)
- Or use Google Sign-In for quick registration

### 2. Login
- Use your email and password
- Or click "Sign in with Google"

### 3. Access Dashboard
After login, you'll be automatically redirected to the dashboard at:
```
http://localhost:5000/dashboard/user
```

## Dashboard Features

### Tab 1: Overview
**What you'll see:**
- 📊 **4 Statistics Cards:**
  - Total Applications count
  - Number of resumes created
  - Tracked jobs count
  - Success rate percentage

- ⚡ **Quick Actions:**
  - Create Resume button
  - Add Job button
  - Track Application button
  - View Kanban Board button

- 📝 **Recent Activity:**
  - Your last 5 job applications
  - Status badges (Applied, Interview, Offer, Rejected)
  - Company names and dates

- 📈 **Application Status:**
  - Progress bars showing application distribution
  - Applied, Interview, Offer, Rejected counts

**Quick Actions:**
```
✓ Click "Create Resume" → Build a new resume
✓ Click "Add Job" → Track a new job listing
✓ Click "Track Application" → Add application record
✓ Click "Kanban View" → See applications in Kanban board
```

### Tab 2: Applications
**What you'll see:**
- 📋 **Applications Table:**
  - Position titles
  - Company names
  - Status badges
  - Application dates
  - Action buttons (View, Edit)

- ➕ **New Application Button:**
  - Creates a new job application entry

**Quick Actions:**
```
✓ Click "New Application" → Create new application
✓ Click View icon → See application details
✓ Click Edit icon → Modify application
✓ Click "View All Applications" → Go to full list
```

### Tab 3: Resumes
**What you'll see:**
- 📄 **Resume Cards:**
  - Resume preview cards
  - Last updated timestamp
  - Action buttons (View, Edit, Download)

- ➕ **Create Resume Button:**
  - Launch resume builder

**Quick Actions:**
```
✓ Click "Create Resume" → Start resume builder
✓ Click View → Preview resume
✓ Click Edit → Modify resume content
✓ Click Download → Export as PDF
```

## Navigation Guide

### Top Header (Always Visible)
- **Left Side:**
  - ☰ Menu toggle (show/hide sidebar)
  - SmartApply logo

- **Middle:**
  - Pricing link
  - Analytics link
  - Profile link

- **Right Side:**
  - 🔍 Search button
  - 🌙 Dark mode toggle
  - 🔔 Notifications (3 new)
  - 👤 User menu dropdown

### Sidebar Menu
**Main Sections:**
- 🏠 Overview (Dashboard home)
- 📄 Resumes
  - My Resumes
  - Resume Builder
- 💼 Applications
  - All Applications
  - Kanban Board
- 🔍 Job Descriptions
- 📊 Analytics

**Account Section:**
- 👤 Profile
- ⚙️ Settings
- 💎 Upgrade

**Support:**
- ❓ Help & FAQ
- 🚪 Logout

## Common Tasks

### Creating Your First Resume
1. Click "Create Resume" from Overview tab or sidebar
2. Fill in personal information
3. Add work experience
4. Add education
5. Add skills
6. Click "Save" or "Generate"

### Tracking a Job Application
1. Go to Applications tab
2. Click "New Application"
3. Enter company name
4. Enter position title
5. Select status (Applied, Interview, Offer, Rejected)
6. Add application date
7. Save the application

### Viewing Application Statistics
1. Click on Overview tab
2. Scroll to "Application Status" section
3. View progress bars for each status
4. Click "View Detailed Analytics" for more insights

### Switching Between Views
- **List View:** Applications tab shows table format
- **Kanban Board:** Click "Kanban View" from Quick Actions
- **Analytics View:** Click Analytics from sidebar

## Keyboard Shortcuts

- **Alt + 1:** Switch to Overview tab
- **Alt + 2:** Switch to Applications tab
- **Alt + 3:** Switch to Resumes tab
- **Ctrl + K:** Open search
- **Ctrl + /:** Toggle dark mode

## Status Badge Colors

- 🔵 **Blue (Primary):** Applied
- 🟡 **Yellow (Warning):** Interview
- 🟢 **Green (Success):** Offer
- ⚪ **Gray (Secondary):** Rejected

## Responsive Design

### Desktop (1200px+)
- Full sidebar visible
- All columns displayed
- 4 statistics cards in one row

### Tablet (768px - 1199px)
- Collapsible sidebar
- 2 statistics cards per row
- Table scrolls horizontally

### Mobile (< 768px)
- Hidden sidebar (toggle to show)
- 1 statistics card per row
- Stacked cards and lists
- Full-width buttons

## Troubleshooting

### Dashboard Not Loading
```bash
# Check if app is running
# Look for "Running on http://0.0.0.0:5000"
```

### Database Connection Error
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env file
# Restart the application
```

### Tabs Not Switching
- Clear browser cache
- Ensure JavaScript is enabled
- Check browser console for errors
- Refresh the page

### Empty Dashboard
- Normal for new accounts
- Click "Create First Application" to get started
- Click "Create First Resume" to begin

## Tips & Best Practices

### For Best Experience:
1. **Update Regularly:** Keep application statuses current
2. **Use Tags:** Tag applications for easy filtering
3. **Track Dates:** Log all important dates
4. **Add Notes:** Keep interview notes in applications
5. **Regular Backups:** Export data periodically

### Workflow Suggestions:
1. **Daily:** Check notifications and update statuses
2. **Weekly:** Review analytics and adjust strategy
3. **Monthly:** Clean up old applications
4. **Ongoing:** Update resume as you gain experience

## Getting Help

### In-App Support
- Click "Help & FAQ" in sidebar
- Use search function to find features
- Check notifications for tips

### Technical Issues
- Check browser console (F12)
- Review Flask application logs
- Verify database connection
- Ensure all dependencies installed

## Next Steps

After getting familiar with the dashboard:
1. ✅ Create your first resume
2. ✅ Add 3-5 job applications
3. ✅ Set up your profile
4. ✅ Explore analytics features
5. ✅ Try Kanban board view
6. ✅ Customize settings
7. ✅ Invite team members (if using Pro)

## Additional Resources

- **User Guide:** Full documentation in `/docs`
- **API Documentation:** For integrations
- **Video Tutorials:** Coming soon
- **Community Forum:** Share tips and tricks

---

**Need Help?** Contact support or check the Help & FAQ section in the dashboard.

**Enjoy SmartApply!** 🚀
