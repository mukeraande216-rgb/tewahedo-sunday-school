from .models import SiteSettings


def church_site(request):
    return {
        "church_site": SiteSettings.objects.first(),
    }
