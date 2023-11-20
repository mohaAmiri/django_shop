from django import forms
from django.contrib.auth.models import User

from accounting.models import Profile

error = {
    'min_length': 'حداقل 5 کاراکتر باشد',
    'required': 'این فیلد اجباری است',
    'invalid': 'ایمیل شما نامعتبر است',
}


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, error_messages=error,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}))
    first_name = forms.CharField(max_length=50, error_messages=error,
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=50, error_messages=error,
                                widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    email = forms.CharField(max_length=50, error_messages=error,
                            widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}))
    password1 = forms.CharField(error_messages=error,
                                widget=forms.PasswordInput(attrs={'placeholder': 'enter password'}))
    password2 = forms.CharField(error_messages=error,
                                widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        ex_user = User.objects.filter(username=username).exists()
        if ex_user:
            raise forms.ValidationError('username has already taken')
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        ex_email = User.objects.filter(email=email).exists()
        email_is_valid = email.find('@')

        if email_is_valid == -1:
            raise forms.ValidationError('this email address is not valid')
        elif ex_email:
            raise forms.ValidationError('this email has already registered')
        else:
            return email

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')

        if len(pass1) < 4:
            raise forms.ValidationError('password is too short')
        elif pass1 != pass2:
            raise forms.ValidationError('password are not similar')
        # elif not any(i.isupper() for i in pass1):
        #     raise forms.ValidationError('password must have at least one capital character')
        else:
            return pass1


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'enter password'}))
    remember = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_image']
