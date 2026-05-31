/*
 * Task Management System - Interactive Logic
 */

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggle');
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Initialize Bootstrap Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Auto-dismiss Alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Handle Form Confirmation
    const confirmActions = document.querySelectorAll('[data-confirm]');
    confirmActions.forEach(element => {
        element.addEventListener('click', (e) => {
            const message = element.getAttribute('data-confirm') || 'Are you sure you want to perform this action?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Dynamic Active Link Highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') !== '#' && currentPath.includes(link.getAttribute('href'))) {
            link.classList.add('active');
        }
    });

    // Password Toggle Utility
    const togglePassword = document.querySelectorAll('.toggle-password');
    togglePassword.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = document.querySelector(this.getAttribute('data-target'));
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.replace('bi-eye', 'bi-eye-slash');
            } else {
                input.type = 'password';
                this.classList.replace('bi-eye-slash', 'bi-eye');
            }
        });
    });
});
