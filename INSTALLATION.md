# INSTALLATION & SETUP GUIDE

Complete step-by-step guide for installing and configuring the Django Task Management System.

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **Database**: SQLite (development) or MySQL 8.0+ (production)
- **RAM**: 2GB minimum
- **Disk Space**: 500MB
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## Step 1: Download/Clone Project

```bash
# Using Git
git clone <repository-url> /path/to/task_management
cd /path/to/task_management

# Or extract ZIP file if downloaded
unzip task_management.zip
cd task_management
```

## Step 2: Create Virtual Environment

### On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### On Windows (Command Prompt):
```bash
python -m venv .venv
.venv\Scripts\activate
```

### On Windows (PowerShell):
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.2.9
- mysqlclient (for MySQL support)
- python-dotenv (for environment variables)
- Pillow (for image handling)
- And other required packages

## Step 4: Configure Environment Variables

### Create .env file:
```bash
cp .env.example .env
```

### Edit .env file with your settings:
```
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# For SQLite (Default Development)
# No additional configuration needed

# For MySQL (Optional - Production)
# Uncomment and modify if using MySQL:
# USE_MYSQL=True
# DB_NAME=task_management
# DB_USER=root
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=3306

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password
```

## Step 5: Initialize Database

### Create migrations:
```bash
python manage.py makemigrations
```

### Apply migrations:
```bash
python manage.py migrate
```

### Initialize default roles and permissions:
```bash
python manage.py init_roles
```

Output should show:
```
Created role: Administrator
Created role: Manager
Created role: Team Lead
Created role: Employee
Created role: Guest
Successfully initialized roles and permissions!
```

## Step 6: Create Superuser Account

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

## Step 7: Collect Static Files (Development)

```bash
python manage.py collectstatic --noinput
```

## Step 8: Start Development Server

```bash
python manage.py runserver
```

You should see:
```
Watching for file changes with StatReloader
Quit the command with CONTROL-C.
Starting development server at http://127.0.0.1:8000/
Django version 5.2.9, using settings 'task_management.settings'
```

## Step 9: Access the Application

Open your browser and visit:

1. **Application**: http://localhost:8000/
2. **Admin Panel**: http://localhost:8000/admin/
3. **Login Page**: http://localhost:8000/accounts/login/

## Step 10: First Login

1. Go to http://localhost:8000/accounts/login/
2. Enter the superuser credentials you created
3. You'll be redirected to the dashboard
4. You now have full admin access!

## Configuration for MySQL (Optional)

### Step 1: Install MySQL

**On macOS (using Homebrew):**
```bash
brew install mysql
brew services start mysql
mysql -u root -p
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install mysql-server
sudo mysql -u root
```

**On Windows:**
Download and install from: https://dev.mysql.com/downloads/mysql/

### Step 2: Create Database and User

```sql
CREATE DATABASE task_management;
CREATE USER 'task_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON task_management.* TO 'task_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Update .env File

```
USE_MYSQL=True
DB_NAME=task_management
DB_USER=task_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=3306
```

### Step 4: Install MySQL Python Connector

```bash
pip install mysqlclient
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py init_roles
```

### Step 6: Start Server

```bash
python manage.py runserver
```

## Troubleshooting Installation

### Issue: "python: command not found"
**Solution**: Use `python3` instead of `python`
```bash
python3 -m venv .venv
python3 manage.py runserver
```

### Issue: "pip: command not found"
**Solution**: Use `pip3` instead of `pip`
```bash
pip3 install -r requirements.txt
```

### Issue: "Virtual environment not activating"
**Solution**: Check the activation script path:
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Make sure virtual environment is activated:
```bash
# Verify virtual environment is active (should see (.venv) in prompt)
which python  # Should show path to .venv/bin/python
pip install -r requirements.txt
```

### Issue: "Permission denied: './manage.py'"
**Solution**: Make file executable:
```bash
chmod +x manage.py
```

### Issue: "MySQLdb installation fails"
**Solution**: Use SQLite instead (default), or install MySQL dev packages:
```bash
# macOS
brew install mysql-client

# Ubuntu/Debian
sudo apt-get install libmysqlclient-dev

# Then retry
pip install mysqlclient
```

### Issue: "Port 8000 already in use"
**Solution**: Use a different port:
```bash
python manage.py runserver 8001
python manage.py runserver 0.0.0.0:8001  # Access from other machines
```

### Issue: "Static files not loading (404 errors)"
**Solution**: Collect static files:
```bash
python manage.py collectstatic --clear --noinput
```

## Project Structure Verification

After installation, verify the project structure:

```
task_management/
├── .env                        ✓ (created from .env.example)
├── .env.example               ✓
├── manage.py                  ✓
├── db.sqlite3                 ✓ (created after migrate)
├── requirements.txt           ✓
├── README.md                  ✓
├── QUICKSTART.md             ✓
├── DEPLOYMENT.md             ✓
├── PROJECT_OVERVIEW.md       ✓
├── setup.sh                   ✓
│
├── task_management/           ✓
│   ├── settings.py           ✓
│   ├── urls.py               ✓
│   ├── wsgi.py               ✓
│   └── asgi.py               ✓
│
├── users/                    ✓
│   ├── models.py             ✓
│   ├── views.py              ✓
│   ├── forms.py              ✓
│   ├── urls.py               ✓
│   ├── admin.py              ✓
│   ├── rbac.py               ✓
│   └── signals.py            ✓
│
├── roles/                    ✓
│   ├── models.py             ✓
│   ├── views.py              ✓
│   ├── forms.py              ✓
│   ├── urls.py               ✓
│   ├── admin.py              ✓
│   └── management/
│       └── commands/
│           └── init_roles.py ✓
│
├── tasks/                    ✓
│   ├── models.py             ✓
│   ├── views.py              ✓
│   ├── forms.py              ✓
│   ├── urls.py               ✓
│   └── admin.py              ✓
│
├── dashboard/                ✓
│   ├── models.py             ✓
│   ├── views.py              ✓
│   ├── urls.py               ✓
│   └── admin.py              ✓
│
├── templates/                ✓ (created after setup)
│   ├── base.html             ✓
│   ├── users/                ✓
│   ├── roles/                ✓
│   ├── tasks/                ✓
│   └── dashboard/            ✓
│
└── static/                   ✓ (created for static files)
```

## Next Steps After Installation

1. **Create test users**:
   - Login as superuser
   - Go to Users → Create User
   - Create test users with different roles

2. **Create test tasks**:
   - Go to Tasks → Create Task
   - Assign tasks to users
   - Test task workflow

3. **Explore features**:
   - Test role-based access
   - Try different dashboards
   - Test task assignment and status updates

4. **Customize for your needs**:
   - Update branding in templates
   - Add custom CSS
   - Configure email settings
   - Set up backups

5. **Plan deployment**:
   - Read DEPLOYMENT.md
   - Choose hosting platform
   - Configure production settings
   - Set up SSL/HTTPS

## Development Tips

### Add new URLs
Edit the app's `urls.py` and main `task_management/urls.py`

### Create new views
Add view functions/classes to app's `views.py` with appropriate decorators

### Add templates
Create HTML files in `templates/<app_name>/` directory

### Run tests
```bash
python manage.py test
python manage.py test users  # Test specific app
```

### Check project health
```bash
python manage.py check
```

### Create data migration
```bash
python manage.py makemigrations --empty users --name initial_data
```

### Open Django shell
```bash
python manage.py shell
>>> from users.models import UserProfile
>>> UserProfile.objects.all()
```

## Backup & Recovery

### Backup database (SQLite):
```bash
cp db.sqlite3 db.sqlite3.backup
```

### Backup project files:
```bash
tar -czf task_management_backup.tar.gz .
```

### Restore database:
```bash
cp db.sqlite3.backup db.sqlite3
```

## Support & Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/5.0/
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html

## Common Development Commands

```bash
# Virtual environment management
source .venv/bin/activate          # Activate
deactivate                         # Deactivate

# Django management
python manage.py runserver        # Start server
python manage.py makemigrations   # Create migrations
python manage.py migrate          # Apply migrations
python manage.py createsuperuser  # Create admin
python manage.py collectstatic    # Collect static files
python manage.py test             # Run tests
python manage.py shell            # Open Python shell

# Package management
pip install <package>             # Install package
pip list                          # List installed packages
pip freeze > requirements.txt     # Update requirements
```

## Performance Optimization

### For Development:
- Use SQLite (default, fast for small projects)
- Enable DEBUG mode for better error messages
- Use Django Debug Toolbar (optional): `pip install django-debug-toolbar`

### For Production:
- Use MySQL for reliability
- Set DEBUG = False
- Enable caching
- Use Gunicorn with multiple workers
- Use Nginx for reverse proxy
- Enable gzip compression
- Use CDN for static files

## Security Best Practices

1. **Never commit sensitive data**:
   - Keep `.env` out of version control
   - Use `.gitignore` to exclude `.env`

2. **Change default passwords**:
   - Always change superuser password
   - Update database password
   - Use strong, unique passwords

3. **Update packages regularly**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --upgrade
   ```

4. **Follow Django security practices**:
   - Keep Django updated
   - Use HTTPS in production
   - Enable CSRF protection
   - Validate all inputs

---

**Version**: 1.0.0  
**Last Updated**: May 31, 2026  
**Status**: Installation Ready

For additional help, refer to README.md, QUICKSTART.md, and the respective documentation files.
