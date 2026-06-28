from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'full_name',
            'date_of_birth',
            'gender',
            'parent',
            'user',
            'allergies_notes',
            'is_active',
            'registration_approved',
        ]