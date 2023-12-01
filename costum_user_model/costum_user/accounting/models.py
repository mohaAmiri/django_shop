from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, phone, password):
        if not email:
            raise ValueError('Email Please')
        if not username:
            raise ValueError('username please')
        if not phone:
            raise ValueError('phone please')
        user = self.model(email=self.normalize_email(email), username=username, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password):
        # * priority is important
        user = self.create_user(email, username, phone, password)



class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # --- define it to use for log in------
    # * field must be unique
    USERNAME_FIELD = 'email'
    # this is for super user
    REQUIRED_FIELDS = ['username', 'phone']
    # -----
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
