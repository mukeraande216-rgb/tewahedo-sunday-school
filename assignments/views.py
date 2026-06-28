from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from classes.models import ClassEnrollment, ClassLevel
from students.models import Parent, Student

from .forms import AssignmentForm, AssignmentReviewForm, AssignmentSubmissionForm
from .models import Assignment, AssignmentSubmission


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


def user_can_view_assignment(user, assignment):
    if user.role == 'admin':
        return True

    if user.role == 'teacher':
        return assignment.class_level_id in get_teacher_class_ids(user)

    if user.role == 'parent':
        try:
            parent = user.parent_profile
            return assignment.class_level_id in list(get_parent_child_class_ids(parent))
        except Parent.DoesNotExist:
            return False

    if user.role == 'student':
        student = getattr(user, 'student_profile', None)
        if not student:
            return False
        return ClassEnrollment.objects.filter(
            student=student,
            class_level=assignment.class_level,
            is_active=True
        ).exists()

    return False


@login_required
def assignment_list(request):
    user = request.user

    if user.role == 'admin':
        assignments = Assignment.objects.select_related(
            'class_level',
            'teacher'
        ).all()

    elif user.role == 'teacher':
        class_ids = get_teacher_class_ids(user)

        assignments = Assignment.objects.select_related(
            'class_level',
            'teacher'
        ).filter(class_level_id__in=class_ids).distinct()

    elif user.role == 'parent':
        try:
            parent = user.parent_profile
            child_class_ids = get_parent_child_class_ids(parent)

            assignments = Assignment.objects.select_related(
                'class_level',
                'teacher'
            ).filter(
                class_level_id__in=child_class_ids,
                is_published=True
            ).distinct()
        except Parent.DoesNotExist:
            assignments = Assignment.objects.none()

    elif user.role == 'student':
        student = getattr(user, 'student_profile', None)
        if student:
            class_ids = ClassEnrollment.objects.filter(
                student=student,
                is_active=True
            ).values_list('class_level_id', flat=True)

            assignments = Assignment.objects.select_related(
                'class_level',
                'teacher'
            ).filter(
                class_level_id__in=class_ids,
                is_published=True
            ).distinct()
        else:
            assignments = Assignment.objects.none()

    else:
        assignments = Assignment.objects.none()

    return render(request, 'assignments/list.html', {'assignments': assignments})


@login_required
def assignment_create(request):
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to create homework.")
        return redirect('assignment_list')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(id__in=allowed_class_ids)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            messages.success(request, "Homework created successfully.")
            return redirect('assignment_list')
    else:
        form = AssignmentForm()

        if request.user.role == 'teacher':
            allowed_class_ids = get_teacher_class_ids(request.user)
            form.fields['class_level'].queryset = ClassLevel.objects.filter(id__in=allowed_class_ids)

    return render(request, 'assignments/create.html', {'form': form})


@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(
        Assignment.objects.select_related('class_level', 'teacher'),
        id=assignment_id
    )

    if not user_can_view_assignment(request.user, assignment):
        messages.error(request, "You do not have permission to view this homework.")
        return redirect('assignment_list')

    submissions = AssignmentSubmission.objects.select_related(
        'student',
        'assignment'
    ).filter(assignment=assignment)

    if request.user.role == 'parent':
        try:
            parent = request.user.parent_profile
            submissions = submissions.filter(student__parent=parent)
        except Parent.DoesNotExist:
            submissions = AssignmentSubmission.objects.none()

    elif request.user.role == 'student':
        student = getattr(request.user, 'student_profile', None)
        if student:
            submissions = submissions.filter(student=student)
        else:
            submissions = AssignmentSubmission.objects.none()

    return render(
        request,
        'assignments/detail.html',
        {
            'assignment': assignment,
            'submissions': submissions,
        }
    )


@login_required
def assignment_submit(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user.role not in ['parent', 'student']:
        messages.error(request, "Only parents or students can submit homework.")
        return redirect('assignment_detail', assignment_id=assignment.id)

    if not user_can_view_assignment(request.user, assignment):
        messages.error(request, "You do not have permission to submit this homework.")
        return redirect('assignment_list')

    available_students = Student.objects.none()

    if request.user.role == 'parent':
        try:
            parent = request.user.parent_profile
            available_students = Student.objects.filter(
                parent=parent,
                enrollments__class_level=assignment.class_level,
                enrollments__is_active=True,
            ).distinct()
        except Parent.DoesNotExist:
            available_students = Student.objects.none()

    elif request.user.role == 'student':
        student = getattr(request.user, 'student_profile', None)
        if student and ClassEnrollment.objects.filter(
            student=student,
            class_level=assignment.class_level,
            is_active=True
        ).exists():
            available_students = Student.objects.filter(id=student.id)

    if not available_students.exists():
        messages.error(request, "No eligible student found for this homework.")
        return redirect('assignment_detail', assignment_id=assignment.id)

    selected_student_id = request.POST.get('student') or request.GET.get('student')
    selected_student = None

    if selected_student_id:
        selected_student = available_students.filter(id=selected_student_id).first()

    if selected_student is None and available_students.count() == 1:
        selected_student = available_students.first()

    if request.method == 'POST':
        if selected_student is None:
            messages.error(request, "Please select a student.")
            form = AssignmentSubmissionForm(request.POST, request.FILES)
        else:
            submission, created = AssignmentSubmission.objects.get_or_create(
                assignment=assignment,
                student=selected_student,
                defaults={
                    'status': AssignmentSubmission.STATUS_NOT_SUBMITTED,
                }
            )

            form = AssignmentSubmissionForm(
                request.POST,
                request.FILES,
                instance=submission
            )

            if form.is_valid():
                submission = form.save(commit=False)
                submission.status = AssignmentSubmission.STATUS_SUBMITTED
                submission.submitted_at = timezone.now()
                submission.save()
                messages.success(request, "Homework submitted successfully.")
                return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = AssignmentSubmissionForm()

    return render(
        request,
        'assignments/submit.html',
        {
            'assignment': assignment,
            'form': form,
            'available_students': available_students,
            'selected_student': selected_student,
        }
    )


@login_required
def assignment_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to review submissions.")
        return redirect('assignment_list')

    if not user_can_view_assignment(request.user, assignment):
        messages.error(request, "You do not have permission to review this homework.")
        return redirect('assignment_list')

    submissions = AssignmentSubmission.objects.select_related(
        'student',
        'assignment'
    ).filter(assignment=assignment)

    return render(
        request,
        'assignments/submissions.html',
        {
            'assignment': assignment,
            'submissions': submissions,
        }
    )


@login_required
def review_submission(request, submission_id):
    submission = get_object_or_404(
        AssignmentSubmission.objects.select_related(
            'assignment',
            'student'
        ),
        id=submission_id
    )

    assignment = submission.assignment

    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, "You do not have permission to review submissions.")
        return redirect('assignment_list')

    if not user_can_view_assignment(request.user, assignment):
        messages.error(request, "You do not have permission to review this submission.")
        return redirect('assignment_list')

    if request.method == 'POST':
        form = AssignmentReviewForm(request.POST, instance=submission)
        if form.is_valid():
            reviewed_submission = form.save(commit=False)
            reviewed_submission.reviewed_by = request.user
            reviewed_submission.reviewed_at = timezone.now()
            reviewed_submission.save()
            messages.success(request, "Submission reviewed successfully.")
            return redirect('assignment_submissions', assignment_id=assignment.id)
    else:
        form = AssignmentReviewForm(instance=submission)

    return render(
        request,
        'assignments/review_submission.html',
        {
            'form': form,
            'submission': submission,
            'assignment': assignment,
        }
    )