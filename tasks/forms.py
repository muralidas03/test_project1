from django import forms
from django.contrib.auth.models import User
from .models import Task, TaskAssignment, TaskComment

class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks
    """
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        empty_label='Unassigned',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Task
        fields = ('title', 'description', 'priority', 'status', 'assigned_to', 'due_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Task Description'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Due Date'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        if due_date:
            from django.utils import timezone
            if due_date < timezone.now():
                raise forms.ValidationError('Due date cannot be in the past.')
        return cleaned_data


class TaskAssignmentForm(forms.Form):
    """
    Form for assigning tasks to users
    """
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select user to assign task to'
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Assignment notes'
        })
    )


class TaskCommentForm(forms.ModelForm):
    """
    Form for adding comments to tasks
    """
    class Meta:
        model = TaskComment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment...'
            })
        }


class TaskFilterForm(forms.Form):
    """
    Form for filtering tasks
    """
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search tasks...'
        })
    )
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Task.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Task.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        empty_label='All Users',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    due_date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    due_date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class TaskStatusUpdateForm(forms.Form):
    """
    Form for updating task status quickly
    """
    status = forms.ChoiceField(
        choices=Task.STATUS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Optional status update notes'
        })
    )
