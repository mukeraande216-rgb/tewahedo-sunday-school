from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_approved', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_approved', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Church School Fields', {'fields': ('role', 'is_approved', 'phone', 'address')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Church School Fields', {'fields': ('role', 'is_approved', 'phone', 'address')}),
    )
