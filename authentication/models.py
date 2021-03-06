from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("Users should have a username")
        if email is None:
            raise TypeError("Users should have a email")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("Password should not be none")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

AUTH_PROVIDER = {
    'facebook': 'facebook',
    'google': 'google',
    'email': 'email',
}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=False, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # other field
    SEX_CHOICES = [("nam", "NAM"), ("nu", "NU")]
    sex = models.CharField(max_length=500, choices=SEX_CHOICES, null=True, blank=True)

    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDER.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        
class LinkModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.TextField(null=False, blank=False)
    image = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)