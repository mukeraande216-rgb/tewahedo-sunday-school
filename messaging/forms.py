from django import forms

from accounts.models import User
from .models import MessageReply, MessageThread


class MessageThreadForm(forms.ModelForm):
    first_message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Type your message here...',
            }
        )
    )

    class Meta:
        model = MessageThread
        fields = [
            'subject',
            'teacher',
            'first_message',
        ]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        teacher_queryset = kwargs.pop('teacher_queryset', None)
        super().__init__(*args, **kwargs)

        if teacher_queryset is not None:
            self.fields['teacher'].queryset = teacher_queryset
        else:
            self.fields['teacher'].queryset = User.objects.filter(role='teacher')


class MessageReplyForm(forms.ModelForm):
    class Meta:
        model = MessageReply
        fields = [
            'body',
            'attachment',
        ]
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Type your reply...',
                }
            ),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }