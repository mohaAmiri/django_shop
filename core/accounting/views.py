from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounting.forms import RegisterForm, LoginForm



def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # if you use create instead of create user, for login you will have an error
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password1'])
            user.is_active = True
            user.save()
    else:
        form = RegisterForm()
    return render(request, 'accounting/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            remember = data['remember']
            try:
                user = authenticate(request, username=User.objects.get(email=data['username']),
                                    password=data['password'])
            except:
                user = authenticate(request, username=data['username'], password=data['password'])

            if user:
                login(request, user)
                # -----remember me----
                if not remember:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(100000)
                messages.success(request, 'successfully logged in', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'username or password is wrong', 'danger')
                return redirect('accounting:login_user')
    else:
        form = LoginForm()

    return render(request, 'accounting/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'successfully logged out', 'primary')
    return redirect('home:home')
