from django import forms
from .models import ClassLevel, ClassEnrollment, ClassGroup


class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = ['name', 'description', 'order', 'is_active', 'teachers']
