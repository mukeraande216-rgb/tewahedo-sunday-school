from django.db import transaction

from django.utils import timezone

from django.contrib import admin

from .models import Member, MembershipApplication


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "member_id",
        "full_name",
        "baptism_name",
        "phone_number",
        "membership_date",
        "is_active",
    )

    list_filter = (
        "is_active",
        "membership_date",
    )

    search_fields = (
        "member_id",
        "full_name",
        "baptism_name",
        "phone_number",
        "address",
        "yenesha_abat",
    )

    ordering = ("full_name",)

    readonly_fields = (
        "member_id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Member Information",
            {
                "fields": (
                    "member_id",
                    "full_name",
                    "baptism_name",
                    "yenesha_abat",
                    "membership_date",
                    "is_active",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "address",
                    "phone_number",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "notes",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "application_id",
        "full_name",
        "phone_number",
        "email",
        "status",
        "submitted_at",
    )

    list_filter = (
        "status",
        "preferred_language",
        "submitted_at",
    )

    search_fields = (
        "application_id",
        "full_name",
        "baptism_name",
        "phone_number",
        "email",
        "address",
    )

    ordering = ("-submitted_at",)

    readonly_fields = (
        "application_id",
        "submitted_at",
        "updated_at",
        "reviewed_at",
        "reviewed_by",
        "approved_member",
    )

    fieldsets = (
        (
            "Application",
            {
                "fields": (
                    "application_id",
                    "status",
                    "submitted_at",
                )
            },
        ),
        (
            "Applicant Information",
            {
                "fields": (
                    "full_name",
                    "baptism_name",
                    "yenesha_abat",
                    "date_of_birth",
                    "preferred_language",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "phone_number",
                    "email",
                    "address",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "household_information",
                    "message",
                    "consent_confirmed",
                )
            },
        ),
        (
            "Administrative Review",
            {
                "fields": (
                    "decision_notes",
                    "reviewed_at",
                    "reviewed_by",
                    "approved_member",
                )
            },
        ),
    )

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if obj.status in {
            MembershipApplication.Status.APPROVED,
            MembershipApplication.Status.REJECTED,
        }:
            obj.reviewed_at = timezone.now()
            obj.reviewed_by = request.user

        super().save_model(request, obj, form, change)

        if (
            obj.status == MembershipApplication.Status.APPROVED
            and obj.approved_member_id is None
        ):
            notes = (
                f"Created from membership application "
                f"{obj.application_id}.\n"
                f"Applicant email: {obj.email}"
            )

            if obj.household_information:
                notes += (
                    f"\nHousehold information: "
                    f"{obj.household_information}"
                )

            if obj.message:
                notes += f"\nApplicant message: {obj.message}"

            member = Member.objects.create(
                full_name=obj.full_name,
                baptism_name=obj.baptism_name,
                yenesha_abat=obj.yenesha_abat,
                address=obj.address,
                phone_number=obj.phone_number,
                membership_date=timezone.localdate(),
                is_active=True,
                notes=notes,
            )

            obj.approved_member = member
            obj.save(
                update_fields=[
                    "approved_member",
                    "updated_at",
                ]
            )
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
