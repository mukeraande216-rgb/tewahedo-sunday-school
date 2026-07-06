from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from classes.models import ClassEnrollment
from .forms import StudentClassEnrollmentForm
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


@login_required
def student_enroll_class(request):
    if request.user.role != 'student':
        messages.error(request, "Only students can enroll in a class from this page.")
        return redirect('dashboard')

    student, created = Student.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'is_active': True,
            'registration_approved': True,
        }
    )

    if request.method == 'POST':
        form = StudentClassEnrollmentForm(request.POST)

        if form.is_valid():
            class_level = form.cleaned_data['class_level']

            enrollment, created = ClassEnrollment.objects.get_or_create(
                student=student,
                class_level=class_level,
                defaults={
                    'is_active': True,
                }
            )

            if not created:
                enrollment.is_active = True
                enrollment.end_date = None
                enrollment.save()

            messages.success(
                request,
                f"You are enrolled in {class_level.name}."
            )

            return redirect('student_list')
    else:
        form = StudentClassEnrollmentForm()

    current_enrollments = ClassEnrollment.objects.select_related(
        'class_level'
    ).filter(
        student=student,
        is_active=True
    )

    return render(
        request,
        'students/enroll_class.html',
        {
            'form': form,
            'student': student,
            'current_enrollments': current_enrollments,
        }
    )