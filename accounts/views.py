from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from students.models import Parent
from .forms import LoginForm, ParentRegistrationForm
from .models import User


def role_based_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.is_approved and not request.user.is_superuser:
        messages.warning(request, "Your account is pending approval by admin.")
        logout(request)
        return redirect('login')

    return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'parent'
            user.is_approved = False
            user.save()

            messages.success(
                request,
                "Registration submitted successfully. Please wait for admin approval."
            )
            return redirect('login')
    else:
        form = ParentRegistrationForm()

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
            elif not user.is_approved and not user.is_superuser:
                messages.error(request, "Your account is pending admin approval.")
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
        messages.error(request, "You do not have permission to view pending registrations.")
        return redirect('dashboard')

    pending_parents = User.objects.filter(
        role='parent',
        is_approved=False
    ).order_by('date_joined')

    return render(
        request,
        'accounts/pending_parents.html',
        {
            'pending_parents': pending_parents,
        }
    )


def approve_parent(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "You do not have permission to approve parents.")
        return redirect('dashboard')

    parent_user = get_object_or_404(
        User,
        id=user_id,
        role='parent'
    )

    parent_user.is_approved = True
    parent_user.save()

    Parent.objects.get_or_create(user=parent_user)

    messages.success(
        request,
        f"{parent_user.get_full_name() or parent_user.username} has been approved."
    )

    return redirect('pending_parent_list')


def reject_parent(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "You do not have permission to reject parents.")
        return redirect('dashboard')

    parent_user = get_object_or_404(
        User,
        id=user_id,
        role='parent',
        is_approved=False
    )

    if request.method == 'POST':
        display_name = parent_user.get_full_name() or parent_user.username
        parent_user.delete()

        messages.success(
            request,
            f"{display_name} registration was rejected and removed."
        )

        return redirect('pending_parent_list')

    return render(
        request,
        'accounts/reject_parent_confirm.html',
        {
            'parent_user': parent_user,
        }
    )


def test_email(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "You do not have permission to send a test email.")
        return redirect('dashboard')

    if not request.user.email:
        messages.error(request, "Your admin user does not have an email address.")
        return redirect('dashboard')

    try:
        send_mail(
            subject='Tewahedo Sunday School Email Test',
            message='This is a test email sent from the live Django app using Zoho SMTP.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            f"Test email sent to {request.user.email}."
        )

    except Exception as error:
        print(f"EMAIL TEST ERROR: {type(error).__name__}: {error}")

        messages.error(
            request,
            f"Email test failed: {type(error).__name__}: {error}"
        )

    return redirect('dashboard')