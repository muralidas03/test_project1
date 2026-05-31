# Quick Start Guide - Task Management System

## 🚀 Get Started in 5 Minutes

This guide will help you get the Task Management System up and running quickly.

### Step 1: Activate Virtual Environment

```bash
cd /Volumes/BB/AWS\ EC2
source .venv/bin/activate
```

On Windows:
```bash
.venv\Scripts\activate
```

### Step 2: Run Development Server

```bash
python manage.py runserver
```

You should see:
```
Watching for file changes with StatReloader
Quit the command with CONTROL-C.
Starting development server at http://127.0.0.1:8000/
```

### Step 3: Access the Application

Open your browser and visit:
- **Application**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

### Step 4: Create Admin User (First Time Only)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: (enter a secure password)
Password (again): (confirm password)
Superuser created successfully.
```

### Step 5: Login

1. Visit http://localhost:8000/accounts/login/
2. Enter your credentials
3. You'll be redirected to the dashboard

## 📚 Default Roles

The system comes with 5 pre-configured roles:

| Role | Features |
|------|----------|
| **Admin** | Full system access, manage everything |
| **Manager** | Manage users and tasks, view reports |
| **Team Lead** | Create and assign tasks, manage team |
| **Employee** | Update assigned tasks, view dashboard |
| **Guest** | View-only access |

## 🎯 Common Tasks

### Create a New User

1. Login as Admin
2. Go to **Users** → **Create User**
3. Fill in the form
4. Select a role
5. Click **Create**

### Create a Task

1. Go to **Tasks** → **Create Task**
2. Fill in task details:
   - Title (required)
   - Description
   - Priority
   - Assign to user
   - Set due date
3. Click **Create Task**

### Assign a Task to User

1. Go to **Tasks** → **[Select Task]**
2. Click **Assign** button
3. Select a user
4. Add notes (optional)
5. Click **Assign**

### Update Task Status

1. Open a task
2. Click **Update Status**
3. Select new status:
   - Pending
   - In Progress
   - Completed
   - On Hold
   - Cancelled
4. Save

### View Dashboard

Dashboards are role-specific:
- **Admin**: System-wide statistics
- **Manager**: Team overview
- **Employee**: Personal task summary

## 🔍 Admin Panel Features

Access Django admin at http://localhost:8000/admin/

In the admin panel you can:
- Create and manage users
- Assign roles
- Create and manage roles
- View all tasks
- Configure permissions
- Manage task assignments

## 🛠️ Useful Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply pending migrations
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic

# Run tests
python manage.py test

# Create admin user
python manage.py createsuperuser

# Initialize roles (already done)
python manage.py init_roles

# Open Django shell
python manage.py shell

# Check project status
python manage.py check
```

## 📊 Project Structure

```
Key Folders:
├── users/          - User management
├── roles/          - Role & permission management
├── tasks/          - Task management
├── dashboard/      - Analytics & reporting
├── templates/      - HTML templates
│   ├── base.html   - Base template
│   ├── users/      - User templates
│   ├── roles/      - Role templates
│   ├── tasks/      - Task templates
│   └── dashboard/  - Dashboard templates
└── static/         - CSS, JS, images
```

## 🔒 Important Notes

### Development vs Production

**Current Setting**: Development (SQLite database)

To switch to MySQL:
1. Install MySQL Server
2. Create database: `CREATE DATABASE task_management;`
3. Edit `.env` file:
   ```
   USE_MYSQL=True
   DB_NAME=task_management
   DB_USER=root
   DB_PASSWORD=your_password
   ```
4. Run migrations: `python manage.py migrate`

### Security Reminders

- Change `SECRET_KEY` in settings for production
- Set `DEBUG = False` before deploying
- Use HTTPS in production
- Keep dependencies updated

## 🆘 Troubleshooting

### Port 8000 already in use

```bash
# Use a different port
python manage.py runserver 8001
```

### Database errors

```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py init_roles
```

### Static files not loading

```bash
python manage.py collectstatic --clear
```

### Can't login

1. Check username/password
2. Verify user account is active
3. Check user has a role assigned

## 📖 Next Steps

1. Read the full [README.md](README.md) for comprehensive documentation
2. Customize templates in `templates/` folder
3. Add custom CSS in `static/css/` folder
4. Create additional users and test workflows
5. Deploy to production using the deployment guide

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [MySQL Tutorial](https://www.mysql.com/resources/)

## 📞 Support

For issues:
1. Check the README.md file
2. Review Django documentation
3. Check terminal error messages
4. Review project settings

---

**Version**: 1.0.0  
**Last Updated**: May 31, 2026  
**Status**: Ready to Use
