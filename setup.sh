#!/bin/bash

# Django Task Management System - Setup Script
# This script automates the setup process

set -e  # Exit on error

echo "=========================================="
echo "Django Task Management System Setup"
echo "=========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 -c 'import sys; assert sys.version_info >= (3, 8)' && echo "  Python 3.8+ detected" || (echo "  ERROR: Python 3.8+ required" && exit 1)

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file from template..."
    cp .env.example .env
    echo "  WARNING: Please edit .env file with your database credentials"
fi

# Run migrations
echo "✓ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Initialize default roles and permissions
echo "✓ Initializing default roles and permissions..."
python manage.py init_roles

# Collect static files
echo "✓ Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Run the development server: python manage.py runserver"
echo "4. Visit http://localhost:8000"
echo ""
echo "For more information, see README.md"
