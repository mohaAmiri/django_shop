from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import *
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ['email', 'username', 'phone']
    list_filter = ['email', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal Info', {'fields': ('is_admin',)}),
        ('Permission', {'fields': ('is_active',)}),

    )

    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'phone', 'password1', 'password2')}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
