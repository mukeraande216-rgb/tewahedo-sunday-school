from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from classes.models import ClassEnrollment
from students.models import Parent

from .forms import MessageReplyForm, MessageThreadForm
from .models import MessageReply, MessageThread


def get_parent_teachers(parent_user):
    try:
        parent = parent_user.parent_profile
    except Parent.DoesNotExist:
        return User.objects.none()

    teacher_ids_from_enrollment = ClassEnrollment.objects.filter(
        student__parent=parent,
        is_active=True,
        teacher__isnull=False
    ).values_list('teacher_id', flat=True)

    teacher_ids_from_class_level = User.objects.filter(
        assigned_class_levels__enrollments__student__parent=parent,
        assigned_class_levels__enrollments__is_active=True,
        role='teacher'
    ).values_list('id', flat=True)

    teacher_ids = list(teacher_ids_from_enrollment) + list(teacher_ids_from_class_level)

    return User.objects.filter(
        id__in=teacher_ids,
        role='teacher'
    ).distinct()


def user_can_view_thread(user, thread):
    if user.role == 'admin':
        return True

    if user.id == thread.parent_id:
        return True

    if user.id == thread.teacher_id:
        return True

    return False


@login_required
def message_list(request):
    user = request.user

    if user.role == 'admin':
        threads = MessageThread.objects.select_related(
            'parent',
            'teacher',
            'created_by'
        ).all()

    elif user.role == 'parent':
        threads = MessageThread.objects.select_related(
            'parent',
            'teacher',
            'created_by'
        ).filter(parent=user)

    elif user.role == 'teacher':
        threads = MessageThread.objects.select_related(
            'parent',
            'teacher',
            'created_by'
        ).filter(teacher=user)

    else:
        threads = MessageThread.objects.none()

    return render(
        request,
        'messaging/list.html',
        {'threads': threads}
    )


@login_required
def message_create(request):
    if request.user.role not in ['parent', 'teacher', 'admin']:
        messages.error(request, "You do not have permission to create messages.")
        return redirect('message_list')

    if request.user.role == 'parent':
        teacher_queryset = get_parent_teachers(request.user)
    else:
        teacher_queryset = User.objects.filter(role='teacher')

    if request.method == 'POST':
        form = MessageThreadForm(
            request.POST,
            teacher_queryset=teacher_queryset
        )

        if form.is_valid():
            thread = form.save(commit=False)

            if request.user.role == 'parent':
                thread.parent = request.user
            else:
                parent_id = request.POST.get('parent')
                parent_user = User.objects.filter(
                    id=parent_id,
                    role='parent'
                ).first()

                if not parent_user:
                    messages.error(request, "Please select a valid parent.")
                    return redirect('message_create')

                thread.parent = parent_user

            thread.created_by = request.user
            thread.save()

            MessageReply.objects.create(
                thread=thread,
                sender=request.user,
                body=form.cleaned_data['first_message']
            )

            messages.success(request, "Message sent successfully.")
            return redirect('message_detail', thread_id=thread.id)

    else:
        form = MessageThreadForm(teacher_queryset=teacher_queryset)

    parent_users = User.objects.filter(role='parent').order_by('first_name', 'last_name', 'username')

    return render(
        request,
        'messaging/create.html',
        {
            'form': form,
            'parent_users': parent_users,
        }
    )


@login_required
def message_detail(request, thread_id):
    thread = get_object_or_404(
        MessageThread.objects.select_related(
            'parent',
            'teacher',
            'created_by'
        ),
        id=thread_id
    )

    if not user_can_view_thread(request.user, thread):
        messages.error(request, "You do not have permission to view this message.")
        return redirect('message_list')

    if request.method == 'POST':
        if thread.is_closed:
            messages.error(request, "This message thread is closed.")
            return redirect('message_detail', thread_id=thread.id)

        form = MessageReplyForm(request.POST, request.FILES)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.sender = request.user
            reply.save()

            thread.save()

            messages.success(request, "Reply sent successfully.")
            return redirect('message_detail', thread_id=thread.id)

    else:
        form = MessageReplyForm()

    replies = thread.replies.select_related('sender').all()

    return render(
        request,
        'messaging/detail.html',
        {
            'thread': thread,
            'replies': replies,
            'form': form,
        }
    )


@login_required
def message_close(request, thread_id):
    thread = get_object_or_404(MessageThread, id=thread_id)

    if request.user.role != 'admin' and request.user.id != thread.teacher_id:
        messages.error(request, "You do not have permission to close this message.")
        return redirect('message_list')

    thread.is_closed = True
    thread.save()

    messages.success(request, "Message thread closed.")
    return redirect('message_detail', thread_id=thread.id)