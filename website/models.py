from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language


def localized(en_value: str, am_value: str) -> str:
    """Return Amharic content when the active language is Amharic and it exists."""
    if (get_language() or "en").startswith("am") and am_value:
        return am_value
    return en_value or am_value


class SiteSettings(models.Model):
    church_name_en = models.CharField(max_length=200, default="St. Urael Ethiopian Orthodox Tewahedo Church")
    church_name_am = models.CharField(max_length=200, blank=True, default="ቅዱስ ኡራኤል ኢትዮጵያዊ ኦርቶዶክስ ተዋሕዶ ቤተ ክርስቲያን")
    short_name = models.CharField(max_length=100, default="St. Urael Church")
    motto_en = models.CharField(max_length=250, blank=True, default="Faith, worship, learning, and community")
    motto_am = models.CharField(max_length=250, blank=True, default="እምነት፣ አምልኮ፣ ትምህርት እና ማኅበረሰብ")
    welcome_en = models.TextField(
        blank=True,
        default="A welcoming Ethiopian Orthodox Tewahedo Christian community serving families, children, youth, and visitors."
    )
    welcome_am = models.TextField(
        blank=True,
        default="ቤተሰቦችን፣ ሕፃናትን፣ ወጣቶችን እና እንግዶችን የሚያገለግል እንግዳ ተቀባይ የኢትዮጵያ ኦርቶዶክስ ተዋሕዶ ክርስቲያናዊ ማኅበረሰብ።"
    )
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    office_hours = models.CharField(max_length=200, blank=True)
    map_url = models.URLField(blank=True)
    livestream_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    donation_url = models.URLField(blank=True)
    sunday_school_url = models.CharField(
        max_length=255,
        blank=True,
        default="/accounts/login/"
    )
    hero_image_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    @property
    def church_name(self):
        return localized(self.church_name_en, self.church_name_am)

    @property
    def motto(self):
        return localized(self.motto_en, self.motto_am)

    @property
    def welcome(self):
        return localized(self.welcome_en, self.welcome_am)

    def __str__(self):
        return self.short_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one SiteSettings record is allowed.")
        super().save(*args, **kwargs)


class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ("info", "Information"),
        ("important", "Important"),
        ("urgent", "Urgent"),
    ]

    title_en = models.CharField(max_length=200)
    title_am = models.CharField(max_length=200, blank=True)
    body_en = models.TextField(blank=True)
    body_am = models.TextField(blank=True)
    link_url = models.URLField(blank=True)
    link_label_en = models.CharField(max_length=80, blank=True)
    link_label_am = models.CharField(max_length=80, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="info")
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-priority", "-starts_at"]

    @property
    def title(self):
        return localized(self.title_en, self.title_am)

    @property
    def body(self):
        return localized(self.body_en, self.body_am)

    @property
    def link_label(self):
        return localized(self.link_label_en, self.link_label_am)

    @property
    def is_current(self):
        now = timezone.now()
        return self.is_published and self.starts_at <= now and (self.ends_at is None or self.ends_at >= now)

    def __str__(self):
        return self.title_en


class ServiceSchedule(models.Model):
    DAY_CHOICES = [
        (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"),
        (4, "Friday"), (5, "Saturday"), (6, "Sunday"),
    ]

    name_en = models.CharField(max_length=150)
    name_am = models.CharField(max_length=150, blank=True)
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    note_en = models.CharField(max_length=250, blank=True)
    note_am = models.CharField(max_length=250, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["day_of_week", "sort_order", "start_time"]

    @property
    def name(self):
        return localized(self.name_en, self.name_am)

    @property
    def note(self):
        return localized(self.note_en, self.note_am)

    def __str__(self):
        return f"{self.get_day_of_week_display()} — {self.name_en}"


class Ministry(models.Model):
    slug = models.SlugField(unique=True)
    name_en = models.CharField(max_length=150)
    name_am = models.CharField(max_length=150, blank=True)
    summary_en = models.TextField()
    summary_am = models.TextField(blank=True)
    audience_en = models.CharField(max_length=150, blank=True)
    audience_am = models.CharField(max_length=150, blank=True)
    image_url = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name_en"]

    @property
    def name(self):
        return localized(self.name_en, self.name_am)

    @property
    def summary(self):
        return localized(self.summary_en, self.summary_am)

    @property
    def audience(self):
        return localized(self.audience_en, self.audience_am)

    def get_absolute_url(self):
        return reverse("website:ministry_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name_en


class Event(models.Model):
    title_en = models.CharField(max_length=200)
    title_am = models.CharField(max_length=200, blank=True)
    description_en = models.TextField(blank=True)
    description_am = models.TextField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    registration_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_at"]

    @property
    def title(self):
        return localized(self.title_en, self.title_am)

    @property
    def description(self):
        return localized(self.description_en, self.description_am)

    @property
    def is_upcoming(self):
        return (self.end_at or self.start_at) >= timezone.now()

    def get_absolute_url(self):
        return reverse("website:event_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title_en


class Sermon(models.Model):
    LANGUAGE_CHOICES = [
        ("am", "Amharic"),
        ("en", "English"),
        ("gez", "Ge'ez"),
        ("mixed", "Mixed"),
    ]

    title_en = models.CharField(max_length=200)
    title_am = models.CharField(max_length=200, blank=True)
    speaker = models.CharField(max_length=150, blank=True)
    scripture_reference = models.CharField(max_length=100, blank=True)
    preached_on = models.DateField()
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="am")
    youtube_url = models.URLField()
    summary_en = models.TextField(blank=True)
    summary_am = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-preached_on"]

    @property
    def title(self):
        return localized(self.title_en, self.title_am)

    @property
    def summary(self):
        return localized(self.summary_en, self.summary_am)

    @property
    def embed_url(self):
        url = self.youtube_url
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return url

    def __str__(self):
        return self.title_en


class ClergyMember(models.Model):
    name = models.CharField(max_length=150)
    title_en = models.CharField(max_length=150)
    title_am = models.CharField(max_length=150, blank=True)
    bio_en = models.TextField(blank=True)
    bio_am = models.TextField(blank=True)
    photo_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    @property
    def title(self):
        return localized(self.title_en, self.title_am)

    @property
    def bio(self):
        return localized(self.bio_en, self.bio_am)

    def __str__(self):
        return self.name


class SacramentalRequest(models.Model):
    SERVICE_CHOICES = [
        ("baptism", "Baptism"),
        ("wedding", "Holy Matrimony"),
        ("memorial", "Memorial / Funeral"),
        ("counseling", "Spiritual Counseling"),
        ("confession", "Confession Appointment"),
        ("certificate", "Certificate / Church Record"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewing", "Reviewing"),
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("closed", "Closed"),
    ]

    service_type = models.CharField(max_length=30, choices=SERVICE_CHOICES)
    requester_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    preferred_date = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True)
    consent_to_contact = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_service_type_display()} — {self.requester_name}"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} — {self.name}"
