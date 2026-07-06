from django import forms

from classes.models import ClassLevel
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

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_of_birth'].required = False
        self.fields['gender'].required = False
        self.fields['parent'].required = False
        self.fields['user'].required = False
        self.fields['allergies_notes'].required = False


class ClassLevelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        teacher_names = [
            teacher.get_full_name() or teacher.username
            for teacher in obj.teachers.all()
        ]

        if teacher_names:
            return f"{obj.name} - Teacher: {', '.join(teacher_names)}"

        return f"{obj.name} - Teacher: Not assigned"


class StudentClassEnrollmentForm(forms.Form):
    class_level = ClassLevelChoiceField(
        queryset=ClassLevel.objects.filter(is_active=True)
        .prefetch_related('teachers')
        .order_by('order', 'name'),
        label='Enroll for',
        empty_label='Choose level and teacher'
    )