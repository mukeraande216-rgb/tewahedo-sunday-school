from django.urls import path

from . import views


app_name = "membership"


urlpatterns = [
    # Public membership application
    path(
        "apply/",
        views.membership_apply,
        name="membership_apply",
    ),
    path(
        "apply/success/<str:application_id>/",
        views.application_success,
        name="application_success",
    ),

    # Private membership application review
    path(
        "applications/",
        views.membership_application_list,
        name="application_list",
    ),

    path(
        "applications/<int:pk>/action/",
        views.membership_application_action,
        name="application_action",
    ),

    # Private membership administration
    path(
        "",
        views.member_list,
        name="member_list",
    ),
    path(
        "add/",
        views.member_create,
        name="member_create",
    ),
    path(
        "import/",
        views.member_import,
        name="member_import",
    ),
    path(
        "export/",
        views.member_export,
        name="member_export",
    ),
    path(
        "<int:pk>/edit/",
        views.member_update,
        name="member_update",
    ),
    path(
        "<int:pk>/deactivate/",
        views.member_deactivate,
        name="member_deactivate",
    ),
]
