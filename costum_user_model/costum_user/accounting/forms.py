from django import forms
from .models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'phone']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] and data['password2'] and data['password1'] != data['password2']:
            raise forms.ValidationError('please check again')
        return data['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ['email', 'username', 'phone']

    def clean_password(self):
        return self.initial['password']
