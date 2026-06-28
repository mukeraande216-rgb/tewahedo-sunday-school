from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from assignments.models import Assignment, AssignmentSubmission
from attendance.models import Attendance
from classes.models import ClassEnrollment
from students.models import Parent, Student


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
def reports_dashboard(request):
    user = request.user

    if user.role == 'admin':
        students = Student.objects.select_related(
            'parent',
            'parent__user'
        ).filter(is_active=True)

    elif user.role == 'teacher':
        class_ids = get_teacher_class_ids(user)

        student_ids = ClassEnrollment.objects.filter(
            class_level_id__in=class_ids,
            is_active=True
        ).values_list('student_id', flat=True)

        students = Student.objects.select_related(
            'parent',
            'parent__user'
        ).filter(
            id__in=student_ids,
            is_active=True
        ).distinct()

    elif user.role == 'parent':
        try:
            parent = user.parent_profile
            students = Student.objects.select_related(
                'parent',
                'parent__user'
            ).filter(
                parent=parent,
                is_active=True
            )
        except Parent.DoesNotExist:
            students = Student.objects.none()

    elif user.role == 'student':
        students = Student.objects.select_related(
            'parent',
            'parent__user'
        ).filter(
            user=user,
            is_active=True
        )

    else:
        students = Student.objects.none()

    report_rows = []

    not_submitted_status = getattr(
        AssignmentSubmission,
        'STATUS_NOT_SUBMITTED',
        'not_submitted'
    )

    present_status = getattr(Attendance, 'STATUS_PRESENT', 'present')
    absent_status = getattr(Attendance, 'STATUS_ABSENT', 'absent')
    late_status = getattr(Attendance, 'STATUS_LATE', 'late')
    excused_status = getattr(Attendance, 'STATUS_EXCUSED', 'excused')

    for student in students:
        class_ids = ClassEnrollment.objects.filter(
            student=student,
            is_active=True
        ).values_list('class_level_id', flat=True)

        total_assignments = Assignment.objects.filter(
            class_level_id__in=class_ids,
            is_published=True
        ).count()

        submission_records = AssignmentSubmission.objects.filter(
            student=student
        )

        submitted_count = submission_records.exclude(
            status=not_submitted_status
        ).count()

        reviewed_count = submission_records.exclude(
            feedback=''
        ).exclude(
            feedback__isnull=True
        ).count()

        missing_homework = max(total_assignments - submitted_count, 0)

        attendance_records = Attendance.objects.filter(student=student)

        attendance_total = attendance_records.count()

        present_count = attendance_records.filter(
            status=present_status
        ).count()

        absent_count = attendance_records.filter(
            status=absent_status
        ).count()

        late_count = attendance_records.filter(
            status=late_status
        ).count()

        excused_count = attendance_records.filter(
            status=excused_status
        ).count()

        if attendance_total > 0:
            attendance_percent = round((present_count / attendance_total) * 100, 1)
        else:
            attendance_percent = 0

        if total_assignments > 0:
            homework_percent = round((submitted_count / total_assignments) * 100, 1)
        else:
            homework_percent = 0

        report_rows.append({
            'student': student,
            'total_assignments': total_assignments,
            'submitted_count': submitted_count,
            'reviewed_count': reviewed_count,
            'missing_homework': missing_homework,
            'homework_percent': homework_percent,
            'attendance_total': attendance_total,
            'present_count': present_count,
            'absent_count': absent_count,
            'late_count': late_count,
            'excused_count': excused_count,
            'attendance_percent': attendance_percent,
        })

    summary = {
        'student_count': students.count(),
        'total_homework': sum(row['total_assignments'] for row in report_rows),
        'total_submitted': sum(row['submitted_count'] for row in report_rows),
        'total_missing': sum(row['missing_homework'] for row in report_rows),
        'total_attendance_records': sum(row['attendance_total'] for row in report_rows),
        'total_present': sum(row['present_count'] for row in report_rows),
        'total_absent': sum(row['absent_count'] for row in report_rows),
    }

    return render(
        request,
        'reports/dashboard.html',
        {
            'report_rows': report_rows,
            'summary': summary,
        }
    )