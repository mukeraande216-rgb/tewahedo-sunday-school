from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from classes.models import ClassEnrollment, ClassLevel
from students.models import Parent

from .forms import AnnouncementForm
from .models import Announcement


def get_teacher_class_ids(user):
    class_ids_from_class_level = user.assigned_class_levels.values_list(
        'id',
        flat=True
    )

    class_ids_from_enrollment = ClassEnrollment.objects.filter(
        teacher=user,
        is_active=True
    ).values_list('class_level_id', flat=True)

    return list(class_ids_from_class_level) + list(class_ids_from_enrollment)


def get_parent_child_class_ids(parent):
    return ClassEnrollment.objects.filter(
        student__parent=parent,
        is_active=True
    ).values_list('class_level_id', flat=True)


def user_can_edit_announcement(user, announcement):
    if user.role == 'admin':
        return True

    if user.role == 'teacher':
        teacher_class_ids = get_teacher_class_ids(user)
        return announcement.class_level_id in teacher_class_ids

    return False


@login_required
def announcement_list(request):
    user = request.user

    if user.role == 'admin':
        announcements = Announcement.objects.select_related(
            'class_level',
            'created_by'
        ).all()

    elif user.role == 'teacher':
        class_ids = get_teacher_class_ids(user)

        announcements = Announcement.objects.select_related(
            'class_level',
            'created_by'
        ).filter(
            is_published=True,
            target='all'
        ) | Announcement.objects.select_related(
            'class_level',
            'created_by'
        ).filter(
            is_published=True,
            class_level_id__in=class_ids
        )

        announcements = announcements.distinct().order_by('-created_at')

    elif user.role == 'parent':
        try:
            parent = user.parent_profile
            class_ids = get_parent_child_class_ids(parent)

            announcements = Announcement.objects.select_related(
                'class_level',
                'created_by'
            ).filter(
                is_published=True,
                target='all'
            ) | Announcement.objects.select_related(
                'class_level',
                'created_by'
            ).filter(
                is_published=True,
                class_level_id__in=class_ids
            )

            announcements = announcements.distinct().order_by('-created_at')

        except Parent.DoesNotExist:
            announcements = Announcement.objects.filter(
                is_published=True,
                target='all'
            ).select_related('class_level', 'created_by')

    elif user.role == 'student':
        student = getattr(user, 'student_profile', None)

        if student:
            class_ids = ClassEnrollment.objects.filter(
                student=student,
                is_active=True
            ).values_list('class_level_id', flat=True)

            announcements = Announcement.objects.select_related(
                'class_level',
                'created_by'
            ).filter(
                is_published=True,
                target='all'
            ) | Announcement.objects.select_related(
                'class_level',
                'created_by'
            ).filter(
                is_published=True,
                class_level_id__in=class_ids
            )

            announcements = announcements.distinct().order_by('-created_at')
        else:
            announcements = Announcement.objects.filter(
                is_published=True,
                target='all'
            ).select_related('class_level', 'created_by')

    else:
        announcements = Announcement.objects.none()

    return render(
        request,
        'announcements/list.html',
        {'announcements': announcements}
    )


@login_required
def announcement_create(request):
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to create announcements.")
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(
                id__in=allowed_class_ids
            )

        if request.user.role == 'admin':
            form.fields['class_level'].queryset = ClassLevel.objects.filter(is_active=True)

        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user

            if request.user.role == 'teacher':
                announcement.target = 'class'

                allowed_class_ids = get_teacher_class_ids(request.user)
                if announcement.class_level_id not in allowed_class_ids:
                    messages.error(request, "You can only post to your assigned class.")
                    return redirect('announcement_create')

            announcement.save()
            messages.success(request, "Announcement created successfully.")
            return redirect('announcement_list')

    else:
        form = AnnouncementForm()

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(
                id__in=allowed_class_ids
            )
            form.fields['target'].initial = 'class'

        if request.user.role == 'admin':
            form.fields['class_level'].queryset = ClassLevel.objects.filter(is_active=True)

    return render(
        request,
        'announcements/create.html',
        {
            'form': form,
            'page_title': 'Create Announcement',
            'button_text': 'Save Announcement',
        }
    )


@login_required
def announcement_edit(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)

    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to edit announcements.")
        return redirect('announcement_list')

    if not user_can_edit_announcement(request.user, announcement):
        messages.error(request, "You can only edit announcements for your assigned class.")
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(
                id__in=allowed_class_ids
            )

        if request.user.role == 'admin':
            form.fields['class_level'].queryset = ClassLevel.objects.filter(is_active=True)

        if form.is_valid():
            updated_announcement = form.save(commit=False)

            if request.user.role == 'teacher':
                updated_announcement.target = 'class'

                allowed_class_ids = get_teacher_class_ids(request.user)
                if updated_announcement.class_level_id not in allowed_class_ids:
                    messages.error(request, "You can only edit announcements for your assigned class.")
                    return redirect('announcement_list')

            updated_announcement.save()
            messages.success(request, "Announcement updated successfully.")
            return redirect('announcement_list')

    else:
        form = AnnouncementForm(instance=announcement)

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(
                id__in=allowed_class_ids
            )

        if request.user.role == 'admin':
            form.fields['class_level'].queryset = ClassLevel.objects.filter(is_active=True)

    return render(
        request,
        'announcements/create.html',
        {
            'form': form,
            'page_title': 'Edit Announcement',
            'button_text': 'Update Announcement',
        }
    )