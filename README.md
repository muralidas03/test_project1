# Django Task Management System with Role-Based Access Control

A comprehensive Task Management System built with Django MVT Architecture, featuring MySQL database, role-based access control, and a complete task workflow management system.

## 🚀 Features

### User Management
- User Registration and Authentication
- User Profile Management
- User Status Management (Active/Inactive/Suspended)
- Search and Filter Users
- User Roles Assignment

### Role Management
- Predefined Roles: Admin, Manager, Team Lead, Employee, Guest
- Dynamic Permission Assignment
- Role-wise Permissions Management
- View Users by Role

### Task Management
- Create, Edit, Delete Tasks
- Task Priority Levels: High, Medium, Low, Urgent
- Task Status: Pending, In Progress, On Hold, Completed, Cancelled
- Task Assignment to Users
- Task Reassignment History
- Task Comments and Notes
- Task Activity Logging

### Role-Based Access Control (RBAC)
- Admin: Full system access
- Manager: Manage users and tasks
- Team Lead: Manage team tasks
- Employee: View and update assigned tasks
- Guest: View-only access

### Dashboard & Analytics
- Admin Dashboard: System-wide statistics
- Manager Dashboard: Team overview
- Employee Dashboard: Personal task summary
- Task Statistics and Reports
- Role-wise Task Distribution
- Priority-wise Task Analysis
- User Performance Metrics

### Security Features
- User Authentication
- Session Management
- CSRF Protection
- Password Validation
- Permission-Based Access Control
- Audit Logging for All Task Changes

## 📋 Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python Package Manager)
- Virtual Environment (recommended)

## 🔧 Installation & Setup

### 1. Clone/Download the Project

```bash
cd /path/to/project
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```
DEBUG=True
SECRET_KEY=your-secret-key-here

# MySQL Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=task_management
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Create MySQL Database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE task_management;
CREATE USER 'task_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON task_management.* TO 'task_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Default Roles and Permissions

```bash
python manage.py init_roles
```

### 8. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 9. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 10. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## 📁 Project Structure

```
task_management/
├── task_management/           # Project configuration
│   ├── settings.py           # Settings and configurations
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── users/                     # User management app
│   ├── models.py             # UserProfile model
│   ├── views.py              # User views
│   ├── forms.py              # User forms
│   ├── urls.py               # User URLs
│   ├── rbac.py               # RBAC decorators
│   ├── signals.py            # Signal handlers
│   └── admin.py              # Admin configuration
│
├── roles/                     # Role management app
│   ├── models.py             # Role and Permission models
│   ├── views.py              # Role views
│   ├── forms.py              # Role forms
│   ├── urls.py               # Role URLs
│   ├── admin.py              # Admin configuration
│   └── management/
│       └── commands/
│           └── init_roles.py # Initialize roles command
│
├── tasks/                     # Task management app
│   ├── models.py             # Task models
│   ├── views.py              # Task views
│   ├── forms.py              # Task forms
│   ├── urls.py               # Task URLs
│   └── admin.py              # Admin configuration
│
├── dashboard/                 # Dashboard app
│   ├── models.py             # Dashboard models
│   ├── views.py              # Dashboard views
│   ├── urls.py               # Dashboard URLs
│   └── admin.py              # Admin configuration
│
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── users/                # User templates
│   ├── roles/                # Role templates
│   ├── tasks/                # Task templates
│   └── dashboard/            # Dashboard templates
│
├── static/                    # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                     # User uploads
│   └── profile_pictures/
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 👥 User Roles & Permissions

### Admin Role
- Full system access
- Create, edit, delete users
- Create, edit, delete roles
- Create, edit, delete tasks
- Assign and reassign tasks
- View system statistics and reports
- Access admin panel

### Manager Role
- View user list
- Create users
- Edit user details
- View all tasks
- Create and assign tasks
- View task statistics
- Generate reports

### Team Lead Role
- View team members
- Create tasks
- Assign tasks to team members
- View task statistics
- Track team progress

### Employee Role
- View assigned tasks
- Update task status
- Add comments to tasks
- View personal dashboard
- Update own profile

### Guest Role
- View-only access
- Can only view tasks and dashboards
- No creation or modification rights

## 🔐 Authentication & Authorization

### Login Page
- Username and password authentication
- Remember me functionality
- Inactive account detection

### Permission Checks
- Decorator-based permission checking
- Role-based access control
- Custom RBAC middleware available

### Example Permission Decorators

```python
from users.rbac import admin_required, role_required, permission_required

@admin_required
def admin_only_view(request):
    # Only admins can access this view
    pass

@role_required('manager')
def manager_only_view(request):
    # Only managers can access this view
    pass

@permission_required('add_task')
def create_task_view(request):
    # Only users with 'add_task' permission
    pass
```

## 📊 Database Schema

### Key Models

#### User Profile
- Extended Django User model
- Stores role, contact info, department, status
- Profile pictures and bio

#### Role
- Role name (admin, manager, team_lead, employee, guest)
- Description
- Active/Inactive status
- Created/Updated timestamps

#### Permission
- Associated with Role
- Permission type (add_user, view_task, etc.)
- Active/Inactive status

#### Task
- Title and description
- Priority (low, medium, high, urgent)
- Status (pending, in_progress, completed, on_hold, cancelled)
- Assigned user
- Created by user
- Due date
- Timestamps

#### Task Assignment
- Tracks assignment history
- Assigned user and date
- Assigned by user
- Current assignment flag
- Notes

#### Task Comment
- Comments on tasks
- Author and timestamp

#### Task Log
- Audit trail for all task changes
- Action type
- Old and new values
- Description

## 🚀 API Endpoints

### Authentication
- `GET/POST /accounts/login/` - User login
- `GET/POST /accounts/register/` - User registration
- `GET /accounts/logout/` - User logout

### User Management
- `GET /accounts/list/` - List all users (admin only)
- `GET/POST /accounts/create/` - Create user (admin only)
- `GET /accounts/<id>/` - View user details (admin only)
- `GET/POST /accounts/<id>/edit/` - Edit user (admin only)
- `POST /accounts/<id>/delete/` - Delete user (admin only)

### Role Management
- `GET /roles/` - List all roles (admin only)
- `GET/POST /roles/create/` - Create role (admin only)
- `GET /roles/<id>/` - View role details (admin only)
- `GET/POST /roles/<id>/edit/` - Edit role (admin only)
- `POST /roles/<id>/delete/` - Delete role (admin only)

### Task Management
- `GET /tasks/` - List tasks (role-based filtering)
- `GET /tasks/<id>/` - View task details
- `GET/POST /tasks/create/` - Create task (manager/admin)
- `GET/POST /tasks/<id>/edit/` - Edit task (admin/creator)
- `POST /tasks/<id>/delete/` - Delete task (admin)
- `GET/POST /tasks/<id>/assign/` - Assign task (admin/manager)
- `POST /tasks/<id>/update-status/` - Update task status
- `POST /tasks/<id>/comment/` - Add comment to task

### Dashboard
- `GET /dashboard/` - Main dashboard (role-based)
- `GET /dashboard/statistics/` - View reports (admin/manager)

## 🎨 Frontend Templates

The application includes Bootstrap 5 templates for:
- Authentication pages (login, register)
- User management (list, create, edit, detail)
- Role management (list, create, edit, permissions)
- Task management (list, create, edit, detail, assign)
- Dashboard (admin, manager, employee views)
- Profile management

### Customizing Templates
All templates extend from `base.html`. To customize styling:
1. Edit `static/css/style.css`
2. Modify Bootstrap classes in templates
3. Override block sections as needed

## ⚙️ Configuration

### Settings.py Configuration

Key settings for production:

```python
# Security
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-secret-key'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'task_management',
        'USER': 'task_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# SSL/HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS (if using API)
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
```

## 📦 Deployment Guide

### Using Gunicorn & Nginx

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Create Systemd Service** (`/etc/systemd/system/taskmanagement.service`)
```ini
[Unit]
Description=Task Management Django Application
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/.venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/path/to/project/gunicorn.sock \
    task_management.wsgi:application

[Install]
WantedBy=multi-user.target
```

3. **Configure Nginx** (`/etc/nginx/sites-available/taskmanagement`)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /path/to/project/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/project/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/project/gunicorn.sock;
    }
}
```

4. **Start Services**
```bash
sudo systemctl enable taskmanagement
sudo systemctl start taskmanagement
sudo systemctl restart nginx
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "task_management.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t taskmanagement .
docker run -p 8000:8000 taskmanagement
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check MySQL is running
sudo service mysql status

# Verify credentials in .env file
# Check database exists: SHOW DATABASES;
```

**Permission Denied for Static Files**
```bash
python manage.py collectstatic --clear --noinput
chmod -R 755 staticfiles/
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Signal Not Registering**
- Ensure `apps.py` has `ready()` method
- Check imports in `apps.py`

## 📈 Performance Tips

1. Use database indexing for frequently queried fields
2. Implement caching for dashboard statistics
3. Use select_related() and prefetch_related() for queries
4. Enable gzip compression in Nginx
5. Use CDN for static files in production

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` in settings
- [ ] Set `DEBUG = False` in production
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS/SSL certificates
- [ ] Set strong database password
- [ ] Configure CORS properly
- [ ] Enable CSRF protection
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Backup database regularly

## 📝 License

This project is provided as-is for educational and development purposes.

## 🤝 Support

For issues, questions, or contributions, please refer to the documentation or contact the development team.

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django RBAC Patterns](https://docs.djangoproject.com/en/stable/topics/auth/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

---

**Version**: 1.0.0  
**Last Updated**: May 31, 2026  
**Status**: Production Ready
