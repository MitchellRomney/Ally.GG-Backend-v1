from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from dashboard.models import AccessCode
from website.forms import SignUpForm
from django.utils import timezone


def home(request):

    # If user is logged in, send them to the dashboard.
    if request.user.is_authenticated:
        return render(request, 'dashboard/home.html', {})

    # If not logged in, send them to the basic homepage.
    return render(request, 'website/home.html', {})


def register(request):

    # If the user is submitting a registration form.
    if request.method == 'POST':

        # Have Django evaluate the form.
        form = SignUpForm(request.POST)
        if form.is_valid():

            # Make sure the Access Code is valid.
            if AccessCode.objects.filter(key=form.cleaned_data.get('key'), used=False, archived=False).count() != 0:

                # Create the new user.
                form.save()

                # Update the Access Code as used and archived.
                access_code = AccessCode.objects.get(key=form.cleaned_data.get('key'))
                access_code.used = True
                access_code.archived = True
                access_code.date_used = timezone.now()

                # Authenticate the user.
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)

                # Assign the user to the Access Code and save the changes.
                access_code.user = user
                access_code.save()

                # Log the user in and send them to the Dashboard homepage.
                login(request, user)
                return redirect('home')
            else:
                # Their access code doesn't work, send them back to the form with an error.
                form = SignUpForm()
                return render(request, 'website/register.html', {
                    'form': form,
                    'failed': True,
                    'message': 'Your entered early access code is not valid.'
                })
    else:
        # Display the registration form.
        form = SignUpForm()
        return render(request, 'website/register.html', {
            'form': form
        })
