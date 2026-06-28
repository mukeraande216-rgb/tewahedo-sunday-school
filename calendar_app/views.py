from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CalendarEventForm
from .models import CalendarEvent


def user_can_manage_calendar(user):
    return user.is_authenticated and user.role in ['admin', 'teacher']


@login_required
def calendar_view(request):
    events = CalendarEvent.objects.select_related(
        'created_by'
    ).all().order_by('start_date', 'title')

    return render(
        request,
        'calendar_app/calendar.html',
        {
            'events': events,
        }
    )


@login_required
def calendar_event_create(request):
    if not user_can_manage_calendar(request.user):
        messages.error(request, "You do not have permission to create calendar events.")
        return redirect('calendar_view')

    if request.method == 'POST':
        form = CalendarEventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()

            messages.success(request, "Calendar event created successfully.")
            return redirect('calendar_view')
    else:
        form = CalendarEventForm()

    return render(
        request,
        'calendar_app/create.html',
        {
            'form': form,
            'page_title': 'Add Calendar Event',
            'button_text': 'Save Event',
        }
    )


@login_required
def calendar_event_edit(request, event_id):
    event = get_object_or_404(CalendarEvent, id=event_id)

    if not user_can_manage_calendar(request.user):
        messages.error(request, "You do not have permission to edit calendar events.")
        return redirect('calendar_view')

    if request.user.role == 'teacher' and event.created_by_id != request.user.id:
        messages.error(request, "Teachers can only edit calendar events they created.")
        return redirect('calendar_view')

    if request.method == 'POST':
        form = CalendarEventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            messages.success(request, "Calendar event updated successfully.")
            return redirect('calendar_view')
    else:
        form = CalendarEventForm(instance=event)

    return render(
        request,
        'calendar_app/create.html',
        {
            'form': form,
            'page_title': 'Edit Calendar Event',
            'button_text': 'Update Event',
        }
    )


@login_required
def calendar_event_delete(request, event_id):
    event = get_object_or_404(CalendarEvent, id=event_id)

    if not user_can_manage_calendar(request.user):
        messages.error(request, "You do not have permission to delete calendar events.")
        return redirect('calendar_view')

    if request.user.role == 'teacher' and event.created_by_id != request.user.id:
        messages.error(request, "Teachers can only delete calendar events they created.")
        return redirect('calendar_view')

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Calendar event deleted successfully.")
        return redirect('calendar_view')

    return render(
        request,
        'calendar_app/delete_confirm.html',
        {
            'event': event,
        }
    )