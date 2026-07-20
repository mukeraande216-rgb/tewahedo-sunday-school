from datetime import time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from website.models import (
    Announcement,
    Event,
    Ministry,
    ServiceSchedule,
    SiteSettings,
)


class Command(BaseCommand):
    help = "Create starter content for the St. Urael church website."

    def handle(self, *args, **options):
        settings, _ = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "address": "Add the official church address",
                "phone": "Add the official telephone number",
                "email": "office@example.org",
                "office_hours": "Contact the church office for current office hours",
            },
        )

        services = [
            {
                "name_en": "Sunday Morning Prayer",
                "name_am": "የእሁድ ጠዋት ጸሎት",
                "day_of_week": 6,
                "start_time": time(5, 0),
                "end_time": time(7, 0),
                "is_featured": True,
                "sort_order": 1,
            },
            {
                "name_en": "Divine Liturgy",
                "name_am": "ቅዳሴ",
                "day_of_week": 6,
                "start_time": time(7, 0),
                "end_time": time(10, 0),
                "is_featured": True,
                "sort_order": 2,
            },
            {
                "name_en": "Sunday School",
                "name_am": "ሰንበት ትምህርት ቤት",
                "day_of_week": 6,
                "start_time": time(10, 30),
                "end_time": time(12, 0),
                "is_featured": True,
                "sort_order": 3,
            },
            {
                "name_en": "Friday Bible Study",
                "name_am": "የዓርብ መጽሐፍ ቅዱስ ጥናት",
                "day_of_week": 4,
                "start_time": time(19, 0),
                "end_time": time(20, 30),
                "is_featured": True,
                "sort_order": 1,
            },
        ]
        for item in services:
            ServiceSchedule.objects.get_or_create(
                name_en=item["name_en"],
                day_of_week=item["day_of_week"],
                defaults=item,
            )

        ministries = [
            (
                "Sunday School",
                "ሰንበት ትምህርት ቤት",
                "Faith formation, Bible education, worship, homework, attendance, and family communication for children and youth.",
                "ለሕፃናትና ለወጣቶች የእምነት ትምህርት፣ መጽሐፍ ቅዱስ፣ አምልኮ፣ የቤት ሥራ፣ ተሳትፎ እና የቤተሰብ ግንኙነት።",
                "Children, youth, parents, and teachers",
                "ሕፃናት፣ ወጣቶች፣ ወላጆች እና መምህራን",
            ),
            (
                "Youth Ministry",
                "የወጣቶች አገልግሎት",
                "Spiritual formation, fellowship, mentoring, service, and leadership opportunities for youth.",
                "ለወጣቶች መንፈሳዊ እድገት፣ ኅብረት፣ ምክር፣ አገልግሎት እና አመራር።",
                "Youth",
                "ወጣቶች",
            ),
            (
                "Choir and Mezmur",
                "መዘምራን",
                "Liturgical singing, mezmur, rehearsal, and service in the worship life of the church.",
                "ቅዳሴ መዝሙር፣ ልምምድ እና በቤተ ክርስቲያን አምልኮ ውስጥ አገልግሎት።",
                "Children, youth, and adults",
                "ሕፃናት፣ ወጣቶች እና አዋቂዎች",
            ),
            (
                "Charity and Community Service",
                "በጎ አድራጎትና ማኅበረሰብ አገልግሎት",
                "Care for families in need, community outreach, volunteering, and coordinated charitable programs.",
                "ለተቸገሩ ቤተሰቦች ድጋፍ፣ የማኅበረሰብ አገልግሎት፣ በጎ ፈቃድ እና የተደራጀ በጎ አድራጎት።",
                "Entire congregation",
                "መላው ምእመናን",
            ),
        ]
        for name_en, name_am, summary_en, summary_am, audience_en, audience_am in ministries:
            Ministry.objects.get_or_create(
                slug=slugify(name_en),
                defaults={
                    "name_en": name_en,
                    "name_am": name_am,
                    "summary_en": summary_en,
                    "summary_am": summary_am,
                    "audience_en": audience_en,
                    "audience_am": audience_am,
                    "is_featured": True,
                },
            )

        Announcement.objects.get_or_create(
            title_en="Welcome to the new St. Urael Church website",
            defaults={
                "title_am": "ወደ አዲሱ የቅዱስ ኡራኤል ቤተ ክርስቲያን ድረ ገጽ እንኳን ደህና መጡ",
                "body_en": "Update the official schedule, contact information, livestream, and giving links in the administration area.",
                "body_am": "በአስተዳደር ገጹ ውስጥ የአገልግሎት ሰዓት፣ የመገናኛ መረጃ፣ የቀጥታ ስርጭት እና የስጦታ አገናኞችን ያዘምኑ።",
                "priority": "important",
            },
        )

        next_sunday = timezone.now() + timedelta(days=(6 - timezone.now().weekday()) % 7 or 7)
        Event.objects.get_or_create(
            title_en="Sunday Divine Liturgy",
            start_at=next_sunday.replace(hour=7, minute=0, second=0, microsecond=0),
            defaults={
                "title_am": "የእሁድ ቅዳሴ",
                "description_en": "Join the church community for prayer, Divine Liturgy, sermon, and fellowship.",
                "description_am": "ለጸሎት፣ ለቅዳሴ፣ ለስብከት እና ለኅብረት ከምእመናን ጋር ይቀላቀሉ።",
                "is_featured": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Starter church website content created."))
