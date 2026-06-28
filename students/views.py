from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from classes.models import ClassEnrollment
from .models import Parent, Student


@login_required
def student_list(request):
    user = request.user

    if user.role == 'admin':
        students = Student.objects.select_related(
            'parent',
            'parent__user'
        ).all()

    elif user.role == 'teacher':
        class_ids_from_class_level = user.assigned_class_levels.values_list(
            'id',
            flat=True
        )

        student_ids_from_teacher_enrollment = ClassEnrollment.objects.filter(
            teacher=user,
            is_active=True
        ).values_list('student_id', flat=True)

        student_ids_from_class_level = ClassEnrollment.objects.filter(
            class_level_id__in=class_ids_from_class_level,
            is_active=True
        ).values_list('student_id', flat=True)

        students = Student.objects.select_related(
            'parent',
            'parent__user'
        ).filter(
            id__in=list(student_ids_from_teacher_enrollment) + list(student_ids_from_class_level)
        ).distinct()

    elif user.role == 'parent':
        try:
            parent = user.parent_profile
            students = Student.objects.select_related(
                'parent',
                'parent__user'
            ).filter(parent=parent)
        except Parent.DoesNotExist:
            students = Student.objects.none()

    elif user.role == 'student':
        students = Student.objects.select_related(
            'parent',
            'parent__user'
        ).filter(user=user)

    else:
        students = Student.objects.none()

    return render(request, 'students/list.html', {'students': students})