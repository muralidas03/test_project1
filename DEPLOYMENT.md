# DEPLOYMENT GUIDE - Task Management System

Comprehensive guide for deploying the Task Management System to production environments.

## 🚀 Pre-Deployment Checklist

- [ ] Update `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up MySQL database
- [ ] Configure SSL/HTTPS
- [ ] Set up static files serving
- [ ] Configure email settings
- [ ] Update database backups
- [ ] Set up monitoring
- [ ] Create superuser account
- [ ] Test all functionality

## 📋 Production Settings Configuration

### settings.py Changes

```python
# ============ SECURITY SETTINGS ============
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'api.yourdomain.com']

# Generate new SECRET_KEY
SECRET_KEY = 'generate-a-new-secure-key-here'

# ============ DATABASE SETTINGS ============
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'task_management_prod',
        'USER': 'task_user',
        'PASSWORD': 'secure_password_here',
        'HOST': 'db.yourdomain.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'max_connections': 100,
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}

# ============ HTTPS/SSL ============
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# ============ LOGGING ============
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/task_management.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'django': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}

# ============ STATIC & MEDIA FILES ============
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/task_management/staticfiles/'
STATICFILES_DIRS = ['/var/www/task_management/static']

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/task_management/media/'

# ============ EMAIL SETTINGS ============
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-specific-password'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'

# ============ CACHE SETTINGS ============
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'task-management-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
```

## 🐧 Linux/Ubuntu Server Deployment

### Step 1: Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-venv python3-pip
sudo apt-get install -y mysql-server mysql-client libmysqlclient-dev
sudo apt-get install -y nginx supervisor git
sudo apt-get install -y certbot python3-certbot-nginx
```

### Step 2: Create Application User

```bash
sudo useradd -m -s /bin/bash taskmanager
sudo usermod -aG sudo taskmanager
```

### Step 3: Set Up Project Directory

```bash
sudo mkdir -p /var/www/task_management
sudo chown taskmanager:taskmanager /var/www/task_management
cd /var/www/task_management

# Clone or upload project
git clone <your-repo> .
# or
# Upload files via SFTP

# Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure MySQL Database

```bash
sudo mysql -u root -p

CREATE DATABASE task_management_prod;
CREATE USER 'task_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON task_management_prod.* TO 'task_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 5: Run Migrations

```bash
cd /var/www/task_management
source .venv/bin/activate

python manage.py migrate
python manage.py init_roles
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 6: Configure Gunicorn

Create `/var/www/task_management/gunicorn_config.py`:

```python
import multiprocessing

bind = "unix:/var/www/task_management/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 100
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
daemon = False
errorlog = "/var/log/django/gunicorn_error.log"
accesslog = "/var/log/django/gunicorn_access.log"
loglevel = "info"
```

### Step 7: Create Systemd Service

Create `/etc/systemd/system/taskmanagement.service`:

```ini
[Unit]
Description=Task Management Django Application
After=network.target mysql.service

[Service]
User=taskmanager
WorkingDirectory=/var/www/task_management
Environment="PATH=/var/www/task_management/.venv/bin"
ExecStart=/var/www/task_management/.venv/bin/gunicorn \
    --config /var/www/task_management/gunicorn_config.py \
    task_management.wsgi:application

Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Step 8: Configure Nginx

Create `/etc/nginx/sites-available/taskmanagement`:

```nginx
upstream django {
    server unix:/var/www/task_management/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 100M;

    location /.well-known/acme-challenge/ {
        root /var/www/task_management;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL certificates (via Certbot)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    client_max_body_size 100M;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_min_length 1024;

    # Static files
    location /static/ {
        alias /var/www/task_management/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/task_management/media/;
        expires 7d;
    }

    # Application
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### Step 9: Enable Services

```bash
# Enable nginx
sudo ln -s /etc/nginx/sites-available/taskmanagement /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Certbot
sudo certbot certonly --webroot -w /var/www/task_management \
    -d yourdomain.com -d www.yourdomain.com

# Enable Gunicorn service
sudo systemctl daemon-reload
sudo systemctl enable taskmanagement
sudo systemctl start taskmanagement
sudo systemctl status taskmanagement
```

### Step 10: Create Log Directories

```bash
sudo mkdir -p /var/log/django
sudo chown taskmanager:taskmanager /var/log/django
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmysqlclient-dev \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m django_user
USER django_user

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "task_management.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: task_management
      MYSQL_USER: task_user
      MYSQL_PASSWORD: task_password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  web:
    build: .
    command: >
      bash -c "python manage.py migrate &&
               python manage.py init_roles &&
               gunicorn --bind 0.0.0.0:8000 --workers 4 task_management.wsgi:application"
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - USE_MYSQL=True
      - DB_HOST=db
      - DB_NAME=task_management
      - DB_USER=task_user
      - DB_PASSWORD=task_password
    depends_on:
      - db
    volumes:
      - ./:/app

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./staticfiles:/app/staticfiles:ro
      - ./media:/app/media:ro
    depends_on:
      - web

volumes:
  mysql_data:
```

### Build and Run

```bash
docker-compose up -d
docker-compose exec web python manage.py createsuperuser
```

## ☁️ AWS EC2 Deployment

### 1. Launch EC2 Instance

- Image: Ubuntu 20.04 LTS
- Instance Type: t3.medium or larger
- Storage: 30GB or more
- Security Group: Allow ports 80, 443

### 2. Install and Configure

Follow the Linux/Ubuntu deployment steps above.

### 3. Configure RDS Database

- Create MySQL RDS instance
- Update DATABASE configuration with RDS endpoint
- Create database and user in RDS

### 4. Configure S3 for Static Files

```python
# settings.py
if not DEBUG:
    AWS_ACCESS_KEY_ID = 'your-key'
    AWS_SECRET_ACCESS_KEY = 'your-secret'
    AWS_STORAGE_BUCKET_NAME = 'your-bucket'
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

Install boto3:
```bash
pip install boto3 django-storages
```

### 5. Set Up CloudFront

- Create CloudFront distribution for static files
- Update STATIC_URL to CloudFront domain

### 6. Use Elastic Beanstalk (Alternative)

```bash
pip install awsebcli
eb init -p python-3.10 task-management
eb create production
eb deploy
```

## 🔄 Backup & Recovery

### MySQL Backup

```bash
# Daily backup
0 2 * * * mysqldump -u task_user -p task_management_prod > /backups/db_$(date +\%Y\%m\%d).sql

# Restore
mysql -u task_user -p task_management_prod < /backups/db_20260101.sql
```

### Media Files Backup

```bash
# Backup media files
0 3 * * * tar -czf /backups/media_$(date +\%Y\%m\%d).tar.gz /var/www/task_management/media/
```

## 📊 Monitoring & Maintenance

### Health Check

```bash
# Check service status
sudo systemctl status taskmanagement
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/django/gunicorn_error.log
sudo tail -f /var/log/django/gunicorn_access.log
```

### Performance Monitoring

- Set up monitoring with Prometheus/Grafana
- Configure alerts for CPU, memory, disk usage
- Monitor application response times
- Track error rates

### Updates & Patches

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Update Python packages
source /var/www/task_management/.venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Restart service
sudo systemctl restart taskmanagement
```

## 🔐 Security Hardening

1. **Firewall Configuration**
   ```bash
   sudo ufw enable
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   ```

2. **SSH Security**
   - Disable root login
   - Use SSH keys instead of passwords
   - Change default SSH port

3. **Regular Updates**
   - Enable automatic security updates
   - Monitor security advisories

4. **Database Security**
   - Enable SSL for database connections
   - Use strong passwords
   - Restrict database access to localhost

## 📈 Scaling Considerations

- Load balancing with multiple Gunicorn workers
- Database connection pooling
- Caching layer (Redis)
- CDN for static files
- Database read replicas for reporting

---

**Version**: 1.0.0  
**Last Updated**: May 31, 2026  
**Status**: Production Ready

For detailed help, refer to the framework documentation and hosting provider guides.
