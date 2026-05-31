from django.core.management.base import BaseCommand
from roles.models import Role, Permission

class Command(BaseCommand):
    help = 'Initialize default roles and permissions'
    
    def handle(self, *args, **options):
        # Define roles
        roles_data = {
            'admin': 'Administrator - Full system access',
            'manager': 'Manager - Manage users and tasks',
            'team_lead': 'Team Lead - Manage team and tasks',
            'employee': 'Employee - View and update assigned tasks',
            'guest': 'Guest - View only access',
        }
        
        # Define permissions for each role
        permissions_map = {
            'admin': [
                'view_user', 'add_user', 'change_user', 'delete_user',
                'view_role', 'add_role', 'change_role', 'delete_role',
                'view_task', 'add_task', 'change_task', 'delete_task', 'assign_task',
                'view_dashboard', 'view_reports', 'admin_access'
            ],
            'manager': [
                'view_user', 'add_user', 'change_user',
                'view_role',
                'view_task', 'add_task', 'change_task', 'assign_task',
                'view_dashboard', 'view_reports'
            ],
            'team_lead': [
                'view_user',
                'view_task', 'add_task', 'change_task', 'assign_task',
                'view_dashboard'
            ],
            'employee': [
                'view_task', 'change_task',
                'view_dashboard'
            ],
            'guest': [
                'view_task',
                'view_dashboard'
            ]
        }
        
        # Create roles and assign permissions
        for role_name, description in roles_data.items():
            role, created = Role.objects.get_or_create(
                name=role_name,
                defaults={'description': description, 'is_active': True}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created role: {role.get_name_display()}')
                )
            
            # Assign permissions
            for permission_code in permissions_map.get(role_name, []):
                # Get or create the permission choice
                permission, perm_created = Permission.objects.get_or_create(
                    role=role,
                    permission=permission_code,
                    defaults={
                        'description': f'{permission_code.replace("_", " ").title()} permission',
                        'is_active': True
                    }
                )
                
                if perm_created:
                    self.stdout.write(f'  Added permission: {permission.get_permission_display()}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully initialized roles and permissions!')
        )
