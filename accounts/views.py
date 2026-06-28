from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from students.models import Parent
from .forms import LoginForm, RegistrationForm


def role_based_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['account_type']
            user.is_approved = True
            user.save()

            if user.role == 'parent':
                Parent.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone': user.phone or '',
                    }
                )

            messages.success(
                request,
                "Registration completed successfully. You can now log in."
            )
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is None:
                messages.error(request, "Invalid username or password.")
            else:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def pending_parent_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "You do not have permission to view registrations.")
        return redirect('dashboard')

    pending_parents = []

    return render(
        request,
        'accounts/pending_parents.html',
        {
            'pending_parents': pending_parents,
        }
    )


def approve_parent(request, user_id):
    messages.info(request, "Approval is no longer required. Users can log in after registration.")
    return redirect('pending_parent_list')


def reject_parent(request, user_id):
    messages.info(request, "Approval is no longer required. Users can log in after registration.")
    return redirect('pending_parent_list')