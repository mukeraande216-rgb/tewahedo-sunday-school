from django import forms
from .models import Assignment, AssignmentSubmission


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'title',
            'description',
            'due_date',
            'class_level',
            'youtube_link',
            'attachment',
            'is_published',
        ]
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                }
            ),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'class_level': forms.Select(attrs={'class': 'form-select'}),
            'youtube_link': forms.URLInput(attrs={'class': 'form-control'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = [
            'response_text',
            'file',
        ]
        widgets = {
            'response_text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Type your homework response here...',
                }
            ),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AssignmentReviewForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = [
            'status',
            'feedback',
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'feedback': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Teacher feedback...',
                }
            ),
        }