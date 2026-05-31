from django import forms
from .models import Role, Permission

class RoleForm(forms.ModelForm):
    """
    Form for creating and updating roles
    """
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text='Select permissions for this role'
    )
    
    class Meta:
        model = Role
        fields = ('name', 'description', 'is_active')
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()


class PermissionForm(forms.ModelForm):
    """
    Form for managing permissions
    """
    class Meta:
        model = Permission
        fields = ('role', 'permission', 'description', 'is_active')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'permission': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RoleFilterForm(forms.Form):
    """
    Form for filtering roles
    """
    name = forms.ChoiceField(
        choices=[('', 'All Roles')] + Role.ROLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.NullBooleanField(
        required=False,
        widget=forms.Select(
            choices=[('', 'All Status'), ('true', 'Active'), ('false', 'Inactive')],
            attrs={'class': 'form-control'}
        )
    )
