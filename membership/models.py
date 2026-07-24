from django.conf import settings
from django.db import models


class Member(models.Model):
    member_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False,
        verbose_name="Member ID",
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name="Full Name",
    )
    baptism_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Baptism Name",
    )
    address = models.TextField(
        blank=True,
        verbose_name="Address",
    )
    yenesha_abat = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Yenesha Abat",
    )
    membership_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Membership Date",
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Phone Number",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Member",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["full_name"]
        indexes = [
            models.Index(fields=["member_id"]),
            models.Index(fields=["full_name"]),
            models.Index(fields=["phone_number"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.member_id:
            generated_id = f"KU{self.pk:06d}"

            type(self).objects.filter(pk=self.pk).update(
                member_id=generated_id
            )

            self.member_id = generated_id

    def __str__(self):
        return f"{self.member_id or 'Pending'} - {self.full_name}"


class MembershipApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        UNDER_REVIEW = "under_review", "Under Review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class PreferredLanguage(models.TextChoices):
        ENGLISH = "en", "English"
        AMHARIC = "am", "Amharic"
        BOTH = "both", "English and Amharic"

    application_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False,
        verbose_name="Application ID",
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name="Full Name",
    )
    baptism_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Baptism Name",
    )
    yenesha_abat = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Yenesha Abat",
    )
    address = models.TextField(
        verbose_name="Address",
    )
    phone_number = models.CharField(
        max_length=30,
        verbose_name="Phone Number",
    )
    email = models.EmailField(
        verbose_name="Email Address",
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of Birth",
    )
    preferred_language = models.CharField(
        max_length=10,
        choices=PreferredLanguage.choices,
        default=PreferredLanguage.BOTH,
        verbose_name="Preferred Language",
    )
    household_information = models.TextField(
        blank=True,
        verbose_name="Family or Household Information",
    )
    message = models.TextField(
        blank=True,
        verbose_name="Additional Message",
    )
    consent_confirmed = models.BooleanField(
        default=False,
        verbose_name="Consent Confirmed",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_membership_applications",
    )
    decision_notes = models.TextField(
        blank=True,
        verbose_name="Decision Notes",
    )
    approved_member = models.OneToOneField(
        Member,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="membership_application",
    )

    class Meta:
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["application_id"]),
            models.Index(fields=["status"]),
            models.Index(fields=["full_name"]),
            models.Index(fields=["submitted_at"]),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.application_id:
            generated_id = f"MA{self.pk:06d}"

            type(self).objects.filter(pk=self.pk).update(
                application_id=generated_id
            )

            self.application_id = generated_id

    def __str__(self):
        return (
            f"{self.application_id or 'Pending'} - "
            f"{self.full_name}"
        )