from django import forms
from django.core.validators import FileExtensionValidator

from .models import Member, MembershipApplication


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "full_name",
            "baptism_name",
            "address",
            "yenesha_abat",
            "membership_date",
            "phone_number",
            "is_active",
            "notes",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "baptism_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "address": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "yenesha_abat": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "membership_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "tel",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class MemberImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Excel membership file",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["xlsx"]
            )
        ],
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": ".xlsx",
            }
        ),
        help_text=(
            "Upload an Excel .xlsx file using the "
            "membership column format."
        ),
    )

    def clean_excel_file(self):
        excel_file = self.cleaned_data["excel_file"]
        max_size = 5 * 1024 * 1024

        if excel_file.size > max_size:
            raise forms.ValidationError(
                "The Excel file must be smaller than 5 MB."
            )

        return excel_file


class MembershipApplicationForm(forms.ModelForm):
    consent_confirmed = forms.BooleanField(
        required=True,
        label=(
            "I confirm that the information provided is accurate "
            "and may be reviewed by authorized church leaders."
        ),
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
    )

    class Meta:
        model = MembershipApplication
        fields = [
            "full_name",
            "baptism_name",
            "yenesha_abat",
            "date_of_birth",
            "phone_number",
            "email",
            "address",
            "preferred_language",
            "household_information",
            "message",
            "consent_confirmed",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your full legal name",
                    "autocomplete": "name",
                }
            ),
            "baptism_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your baptism name, if applicable",
                }
            ),
            "yenesha_abat": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Yenesha Abat, if applicable",
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "tel",
                    "placeholder": "(000) 000-0000",
                    "autocomplete": "tel",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name@example.com",
                    "autocomplete": "email",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Street, city, state, and ZIP code",
                    "autocomplete": "street-address",
                }
            ),
            "preferred_language": forms.Select(
                attrs={"class": "form-select"}
            ),
            "household_information": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": (
                        "List family or household members, if applicable"
                    ),
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Share any additional information or questions"
                    ),
                }
            ),
        }

    def clean_full_name(self):
        return self.cleaned_data["full_name"].strip()

    def clean_phone_number(self):
        return self.cleaned_data["phone_number"].strip()

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()