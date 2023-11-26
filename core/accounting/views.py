from random import randint
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from six import text_type

from accounting.forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, PhoneForm, CodeForm
from accounting.models import Profile


# ---------------------verification account with email---------------------
class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_generator = EmailToken()


class RegisterEmail(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'User successfully activated!', 'success')
            return redirect('accounting:login_user')


# -------------------------------------------------------------------------


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
            user.is_active = False
            user.save()
            # ----------------activation email-----------
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounting:active-account',
                          kwargs={'uidb64': uidb64, 'token': email_generator.make_token(user)})
            link = 'http://' + domain + url
            # ----------------sending email--------------
            email = EmailMessage(
                'active user',  # title of email
                link,  # content of email
                'test<amirimohammad117@gmail.com>',  # name of email
                [data['email']],  # the email address which we want to send email
            )
            email.send(fail_silently=False)
            # --------------------------------------------
            messages.success(request, 'email sent', 'success')
            return redirect('home:home')
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


@login_required(login_url='accounting:login_user')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'accounting/profile.html', {'profile': profile})


@login_required(login_url='accounting:login_user')
def update_profile(request):
    if request.method == 'POST':
        update_user_form = UpdateUserForm(request.POST, instance=request.user)
        update_profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if update_profile_form and update_profile_form.is_valid():
            update_user_form.save()
            update_profile_form.save()
            messages.success(request, 'successfully updated', 'success')
            return redirect('accounting:profile')
    else:
        update_user_form = UpdateUserForm(instance=request.user)
        update_profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {'user_form': update_user_form, 'profile_form': update_profile_form}
    return render(request, 'accounting/update.html', context)


@login_required(login_url='accounting:login_user')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'password successfully changed', 'success')
        else:
            messages.error(request, 'password is wrong', 'danger')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounting/changePassword.html', {'form': form})


def phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            global random_code, phone
            data = form.cleaned_data
            phone = f"0{data['phone']}"
            random_code = randint(100, 1000)
            print(random_code, phone)
            # -------------kavenegar api for sending message ---------------------------
            # api = KavenegarAPI(
            #     '42563968306266646633697931444F2B35736D6B73724545316F4E58314931714F394171363934453369303D')
            # params = {'sender': '10008663', 'receptor': phone, 'message': random_code}
            # api.sms_send(params)
            # ------------------------------------------------------------------------------
            return redirect('accounting:verify')
    else:
        form = PhoneForm()
    return render(request, 'accounting/phone_login.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if random_code == data['code']:
                try:
                    profile = Profile.objects.get(phone=phone)
                except ObjectDoesNotExist:
                    messages.success(request, 'User with this phone number does not exist', 'danger')
                    return redirect('accounting:phone_login')
                print(profile)
                user = User.objects.get(profile__id=profile.id)
                login(request, user)
                messages.success(request, 'successfully logged in', 'success')
                return redirect('home:home')
            else:
                messages.success(request, 'the entered code is wrong', 'danger')
    else:
        form = CodeForm()
    return render(request, 'accounting/verify.html', {'form': form})


# --------------------------------password Change------------------------------------
class ResetPassword(auth_views.PasswordResetView):
    template_name = 'accounting/reset.html'
    success_url = reverse_lazy('accounting:reset-done')
    email_template_name = 'accounting/link.html'


class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'accounting/done.html'


class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounting/confirm.html'
    success_url = reverse_lazy('accounting:complete')


class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounting/complete.html'

# ------------------------------------------------------------------------------------
