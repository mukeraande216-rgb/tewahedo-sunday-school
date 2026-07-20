from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from .forms import ContactForm, SacramentalRequestForm
from .models import (
    Announcement,
    ClergyMember,
    Event,
    Ministry,
    Sermon,
    ServiceSchedule,
    SiteSettings,
)


def _settings():
    return SiteSettings.objects.first()


def home(request):
    now = timezone.now()
    announcements = [a for a in Announcement.objects.filter(is_published=True) if a.is_current][:3]
    context = {
        "settings": _settings(),
        "announcements": announcements,
        "featured_services": ServiceSchedule.objects.filter(is_active=True, is_featured=True)[:4],
        "upcoming_events": Event.objects.filter(
            is_published=True
        ).filter(
            Q(end_at__gte=now) | Q(end_at__isnull=True, start_at__gte=now)
        ).order_by("start_at")[:3],
        "featured_ministries": Ministry.objects.filter(is_active=True, is_featured=True)[:6],
        "latest_sermon": Sermon.objects.filter(is_published=True).first(),
    }
    return render(request, "website/home.html", context)


def about(request):
    return render(
        request,
        "website/about.html",
        {"clergy_members": ClergyMember.objects.filter(is_active=True)},
    )


def schedule(request):
    return render(
        request,
        "website/schedule.html",
        {"services": ServiceSchedule.objects.filter(is_active=True)},
    )


def ministries(request):
    return render(
        request,
        "website/ministries.html",
        {"ministries": Ministry.objects.filter(is_active=True)},
    )


def ministry_detail(request, slug):
    ministry = get_object_or_404(Ministry, slug=slug, is_active=True)
    return render(request, "website/ministry_detail.html", {"ministry": ministry})


def events(request):
    now = timezone.now()
    upcoming = Event.objects.filter(is_published=True).filter(
        Q(end_at__gte=now) | Q(end_at__isnull=True, start_at__gte=now)
    ).order_by("start_at")
    return render(request, "website/events.html", {"events": upcoming})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_published=True)
    return render(request, "website/event_detail.html", {"event": event})


def sermons(request):
    queryset = Sermon.objects.filter(is_published=True)
    language = request.GET.get("language")
    if language:
        queryset = queryset.filter(language=language)
    return render(request, "website/sermons.html", {"sermons": queryset, "selected_language": language})


def livestream(request):
    latest_sermon = Sermon.objects.filter(is_published=True).first()
    return render(
        request,
        "website/livestream.html",
        {"settings": _settings(), "latest_sermon": latest_sermon},
    )


def new_here(request):
    return render(
        request,
        "website/new_here.html",
        {
            "settings": _settings(),
            "featured_services": ServiceSchedule.objects.filter(is_active=True, is_featured=True)[:4],
        },
    )


@require_http_methods(["GET", "POST"])
def sacraments(request):
    form = SacramentalRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            _("Your request was submitted. The church office will contact you after reviewing it."),
        )
        return redirect("website:sacraments")
    return render(request, "website/sacraments.html", {"form": form})


def give(request):
    return render(request, "website/give.html", {"settings": _settings()})


@require_http_methods(["GET", "POST"])
def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Thank you. Your message was sent to the church office."))
        return redirect("website:contact")
    return render(request, "website/contact.html", {"form": form, "settings": _settings()})
