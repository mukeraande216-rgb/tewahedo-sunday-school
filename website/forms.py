from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactSubmission, SacramentalRequest


class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            css_class = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            field.widget.attrs["class"] = f'{field.widget.attrs.get("class", "")} {css_class}'.strip()
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("placeholder", field.label)


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
        labels = {
            "name": _("Full name"),
            "email": _("Email"),
            "phone": _("Phone"),
            "subject": _("Subject"),
            "message": _("Message"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class SacramentalRequestForm(BootstrapFormMixin, forms.ModelForm):
    consent_to_contact = forms.BooleanField(
        required=True,
        label=_("I authorize the church office to contact me about this request."),
    )

    class Meta:
        model = SacramentalRequest
        fields = [
            "service_type", "requester_name", "email", "phone",
            "preferred_date", "details", "consent_to_contact",
        ]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "details": forms.Textarea(attrs={"rows": 5}),
        }
        labels = {
            "service_type": _("Requested service"),
            "requester_name": _("Full name"),
            "email": _("Email"),
            "phone": _("Phone"),
            "preferred_date": _("Preferred date"),
            "details": _("Additional details"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
