from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from classes.models import ClassEnrollment, ClassLevel
from students.models import Parent

from .forms import ResourceForm
from .models import Resource


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


def user_can_manage_resource(user, resource):
    if user.role == 'admin':
        return True

    if user.role == 'teacher':
        teacher_class_ids = get_teacher_class_ids(user)

        return (
            resource.uploaded_by_id == user.id
            and resource.class_level_id in teacher_class_ids
        )

    return False


@login_required
def resource_list(request):
    user = request.user

    if user.role == 'admin':
        resources = Resource.objects.select_related(
            'class_level',
            'uploaded_by'
        ).all()

    elif user.role == 'teacher':
        class_ids = get_teacher_class_ids(user)

        all_resources = Resource.objects.select_related(
            'class_level',
            'uploaded_by'
        ).filter(
            is_published=True,
            class_level__isnull=True
        )

        class_resources = Resource.objects.select_related(
            'class_level',
            'uploaded_by'
        ).filter(
            is_published=True,
            class_level_id__in=class_ids
        )

        resources = (all_resources | class_resources).distinct().order_by('-created_at')

    elif user.role == 'parent':
        try:
            parent = user.parent_profile
            class_ids = get_parent_child_class_ids(parent)

            all_resources = Resource.objects.select_related(
                'class_level',
                'uploaded_by'
            ).filter(
                is_published=True,
                class_level__isnull=True
            )

            class_resources = Resource.objects.select_related(
                'class_level',
                'uploaded_by'
            ).filter(
                is_published=True,
                class_level_id__in=class_ids
            )

            resources = (all_resources | class_resources).distinct().order_by('-created_at')

        except Parent.DoesNotExist:
            resources = Resource.objects.filter(
                is_published=True,
                class_level__isnull=True
            ).select_related('class_level', 'uploaded_by')

    elif user.role == 'student':
        student = getattr(user, 'student_profile', None)

        if student:
            class_ids = ClassEnrollment.objects.filter(
                student=student,
                is_active=True
            ).values_list('class_level_id', flat=True)

            all_resources = Resource.objects.select_related(
                'class_level',
                'uploaded_by'
            ).filter(
                is_published=True,
                class_level__isnull=True
            )

            class_resources = Resource.objects.select_related(
                'class_level',
                'uploaded_by'
            ).filter(
                is_published=True,
                class_level_id__in=class_ids
            )

            resources = (all_resources | class_resources).distinct().order_by('-created_at')

        else:
            resources = Resource.objects.filter(
                is_published=True,
                class_level__isnull=True
            ).select_related('class_level', 'uploaded_by')

    else:
        resources = Resource.objects.none()

    return render(
        request,
        'resources/list.html',
        {'resources': resources}
    )


@login_required
def resource_create(request):
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to upload resources.")
        return redirect('resource_list')

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(
                id__in=allowed_class_ids
            )

        if request.user.role == 'admin':
            form.fields['class_level'].queryset = ClassLevel.objects.filter(is_active=True)

        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user

            if request.user.role == 'teacher':
                allowed_class_ids = get_teacher_class_ids(request.user)

                if resource.class_level_id not in allowed_class_ids:
                    messages.error(request, "Teachers can only upload resources for their assigned class.")
                    return redirect('resource_create')

            resource.save()
            messages.success(request, "Resource uploaded successfully.")
            return redirect('resource_list')

    else:
        form = ResourceForm()

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(
                id__in=allowed_class_ids
            )

        if request.user.role == 'admin':
            form.fields['class_level'].queryset = ClassLevel.objects.filter(is_active=True)

    return render(
        request,
        'resources/create.html',
        {
            'form': form,
            'page_title': 'Upload Resource',
            'button_text': 'Save Resource',
        }
    )


@login_required
def resource_edit(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)

    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to edit resources.")
        return redirect('resource_list')

    if not user_can_manage_resource(request.user, resource):
        messages.error(request, "You can only edit resources you uploaded for your assigned class.")
        return redirect('resource_list')

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(
                id__in=allowed_class_ids
            )

        if request.user.role == 'admin':
            form.fields['class_level'].queryset = ClassLevel.objects.filter(is_active=True)

        if form.is_valid():
            updated_resource = form.save(commit=False)

            if request.user.role == 'teacher':
                allowed_class_ids = get_teacher_class_ids(request.user)

                if updated_resource.class_level_id not in allowed_class_ids:
                    messages.error(request, "Teachers can only edit resources for their assigned class.")
                    return redirect('resource_list')

            updated_resource.save()
            messages.success(request, "Resource updated successfully.")
            return redirect('resource_list')

    else:
        form = ResourceForm(instance=resource)

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(
                id__in=allowed_class_ids
            )

        if request.user.role == 'admin':
            form.fields['class_level'].queryset = ClassLevel.objects.filter(is_active=True)

    return render(
        request,
        'resources/create.html',
        {
            'form': form,
            'page_title': 'Edit Resource',
            'button_text': 'Update Resource',
        }
    )


@login_required
def resource_delete(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)

    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to delete resources.")
        return redirect('resource_list')

    if not user_can_manage_resource(request.user, resource):
        messages.error(request, "You can only delete resources you uploaded for your assigned class.")
        return redirect('resource_list')

    if request.method == 'POST':
        resource.delete()
        messages.success(request, "Resource deleted successfully.")
        return redirect('resource_list')

    return render(
        request,
        'resources/delete_confirm.html',
        {'resource': resource}
    )