from datetime import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import secrets
import phonenumbers
from django.core.validators import MinLengthValidator
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from typing import Optional, Tuple


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        abstract = True

    def activate_user(self):
        if not self.is_active:
            self.is_active = True
            self.activated_at = timezone.now()
            self.save(update_fields=["is_active", "activated_at"])

    def deactivate_user(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active"])


class CustomerManager(BaseUserManager):
    def create_via_whatsapp(
        self, phone_number, name
    ) -> Tuple["CustomerUser", str, bool]:
        phone_number = self.normalize_phone(phone_number)

        try:
            customer = self.get(phone_number=phone_number)
            if customer.token_expires_at < timezone.now():
                token = customer.generate_new_token()
            else:
                token = customer.access_token
            return customer, token, False
        except CustomerUser.DoesNotExist:
            token = self.generate_access_token()
            customer = self.create(
                phone_number=phone_number,
                name=f"Customer-{phone_number[-4]}",
                access_token=token,
                is_active=True,
                token_expires_at=timezone.now() + timezone.timedelta(minutes=15),
            )
            return customer, token, True

    def validate_token(self, token) -> Optional["CustomerUser"]:
        try:
            customer = self.get(access_token=token)
            if customer.token_expires_at >= timezone.now():
                return customer
            return None
        except CustomerUser.DoesNotExist:
            return None

    def normalize_phone(self, phone) -> str:
        try:
            parsed = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed):
                raise ValidationError("Invalid phone number")
            return phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.NumberParseException:
            raise ValidationError("Invalid phone number format")

    def generate_access_token(self):

        return secrets.token_urlsafe(32)


class CustomerUser(BaseUser):
    phone_number = models.CharField(
        max_length=20, unique=True, validators=[MinLengthValidator(10)]
    )
    access_token = models.CharField(max_length=44, unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)

    objects = CustomerManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def clean(self):
        super().clean()
        try:
            parsed = phonenumbers.parse(self.phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                raise ValidationError("Invalid phone number")
        except phonenumbers.NumberParseException:
            raise ValidationError("Invalid phone number format")

    def generate_new_token(self) -> str:
        self.access_token = CustomerManager().generate_access_token()
        self.token_expires_at = timezone.now() + timezone.timedelta(minutes=15)
        self.save()
        return self.access_token


class LoginAttempt(models.Model):
    user = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="login_attempt"
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    location = gis_models.PointField(geography=True, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    token_used = models.CharField(max_length=44)

    class Meta:
        ordering = "-timestamp"


class ManagerUserRoles(models.TextChoices):
    FULL_CONTROL = "full_control", "Full Control"
    PRODUCT_MANAGER = "product_manager", "Product Manager"
    STOCK_MANAGER = "stock_manager", "Stock Manager"
    BASE_ACCESS = "base_access", "Base Access"


class ManagerUser(BaseUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=ManagerUserRoles.choices,
        default=ManagerUserRoles.BASE_ACCESS,
    )
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "role"]

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

    def __str__(self):
        return f"Manager: {self.email}"

    def save(self, *args, **kwargs):

        self.is_active = True
        super().save(*args, **kwargs)
