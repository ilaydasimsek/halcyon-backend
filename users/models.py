import random
import string
from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Adapted from: https://koenwoortman.com/python-django-email-as-username/
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        validate_password(raw_password)
        super().set_password(raw_password)

    def reset_password(self, new_password, verification_code: str):
        with transaction.atomic():
            verification_obj = PasswordResetVerification.objects.filter(user=self, code=verification_code).first()
            if not verification_obj or verification_obj.is_expired():
                raise PermissionError(_("Invalid verification code"))
            self.set_password(new_password)
            self.save()
            verification_obj.delete()


class PasswordResetVerification(models.Model):
    EXPIRY_IN_MINUTES = 5
    CODE_LENGTH = 6

    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def is_expired(self) -> bool:
        return self.created_at + timedelta(minutes=self.EXPIRY_IN_MINUTES) < timezone.now()

    @staticmethod
    def create_for_user(user: User) -> "PasswordResetVerification":
        with transaction.atomic():
            PasswordResetVerification.objects.filter(user=user).delete()
            code = ''.join(random.choices(string.digits, k=PasswordResetVerification.CODE_LENGTH))
            return PasswordResetVerification.objects.create(user=user, code=code)
    @staticmethod
    def is_code_valid(user: User, code: str) -> bool:
        obj = PasswordResetVerification.objects.filter(user=user, code=code).first()
        return not obj.is_expired() if obj else False
