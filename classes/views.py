from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ClassLevel


@login_required
def class_list(request):
    class_levels = ClassLevel.objects.all()
    return render(request, 'classes/list.html', {'class_levels': class_levels})
