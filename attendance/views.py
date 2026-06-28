from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from classes.models import ClassEnrollment, ClassLevel
from students.models import Parent, Student
from .models import Attendance


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


@login_required
def attendance_list(request):
    user = request.user

    if user.role == 'admin':
        attendance_records = Attendance.objects.select_related(
            'student',
            'marked_by'
        ).all()

    elif user.role == 'teacher':
        class_ids = get_teacher_class_ids(user)

        student_ids = ClassEnrollment.objects.filter(
            class_level_id__in=class_ids,
            is_active=True
        ).values_list('student_id', flat=True)

        attendance_records = Attendance.objects.select_related(
            'student',
            'marked_by'
        ).filter(student_id__in=student_ids)

    elif user.role == 'parent':
        try:
            parent = user.parent_profile
            attendance_records = Attendance.objects.select_related(
                'student',
                'marked_by'
            ).filter(student__parent=parent)
        except Parent.DoesNotExist:
            attendance_records = Attendance.objects.none()

    elif user.role == 'student':
        student = getattr(user, 'student_profile', None)
        if student:
            attendance_records = Attendance.objects.select_related(
                'student',
                'marked_by'
            ).filter(student=student)
        else:
            attendance_records = Attendance.objects.none()

    else:
        attendance_records = Attendance.objects.none()

    return render(
        request,
        'attendance/list.html',
        {'attendance_records': attendance_records}
    )


@login_required
def take_attendance(request):
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to take attendance.")
        return redirect('attendance_list')

    selected_class_id = request.GET.get('class_level') or request.POST.get('class_level')
    session_date = request.GET.get('session_date') or request.POST.get('session_date')

    if not session_date:
        session_date = timezone.localdate().isoformat()

    if request.user.role == 'admin':
        class_levels = ClassLevel.objects.filter(is_active=True)
    else:
        class_ids = get_teacher_class_ids(request.user)
        class_levels = ClassLevel.objects.filter(id__in=class_ids, is_active=True)

    selected_class = None
    students = Student.objects.none()

    if selected_class_id:
        selected_class = class_levels.filter(id=selected_class_id).first()

        if selected_class:
            student_ids = ClassEnrollment.objects.filter(
                class_level=selected_class,
                is_active=True
            ).values_list('student_id', flat=True)

            students = Student.objects.filter(
                id__in=student_ids,
                is_active=True
            ).order_by('full_name')

    if request.method == 'POST':
        if not selected_class:
            messages.error(request, "Please select a valid class.")
            return redirect('take_attendance')

        for student in students:
            status = request.POST.get(f'status_{student.id}')
            notes = request.POST.get(f'notes_{student.id}', '')

            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    session_date=session_date,
                    defaults={
                        'status': status,
                        'notes': notes,
                        'marked_by': request.user,
                    }
                )

        messages.success(request, "Attendance saved successfully.")
        return redirect('attendance_list')

    existing_attendance = {}
    if selected_class and session_date:
        records = Attendance.objects.filter(
            student__in=students,
            session_date=session_date
        )

        existing_attendance = {
            record.student_id: record
            for record in records
        }

    return render(
        request,
        'attendance/take.html',
        {
            'class_levels': class_levels,
            'selected_class': selected_class,
            'selected_class_id': selected_class_id,
            'session_date': session_date,
            'students': students,
            'existing_attendance': existing_attendance,
            'status_choices': Attendance.STATUS_CHOICES,
        }
    )