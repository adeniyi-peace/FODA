# from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
# from django.db import models

# # Create your models here.

# class VendorManager(UserManager):
#     def _create_vendor(self, email,password,**extra_fields):
#         """
#         Create and return a Vendor with an email and password.
#         """
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         vendor = self.model(email=email, **extra_fields)
#         vendor.set_password(password)
#         vendor.save(using=self._db)
#         return vendor
#     def create_vendor(self, email=None, password=None, **extra_fields):
#         """
#         Create and return a Vendor with an email and password.
#         """
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_vendor(email, password, **extra_fields)
    
   
    
# class Vendor(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=30, blank=True)
#     location = models.CharField(max_length=255, blank=True)
#     contact_info = models.CharField(max_length=100, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     last_login = models.DateTimeField(auto_now=True)

#     objects = VendorManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = 'vendor'
#         verbose_name_plural = 'vendors'
#         ordering = ['email']

#     def __str__(self):
#         return self.email

#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}".strip()

#     def get_short_name(self):
#         return self.first_name or self.email

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class VendorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Vendors must have an email address")
        email = self.normalize_email(email)
        vendor = self.model(email=email, **extra_fields)
        vendor.set_password(password)
        vendor.save(using=self._db)
        return vendor

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Vendor(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    shop_name = models.CharField(max_length=255,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['shop_name']

    objects = VendorManager()

    def __str__(self):
        return self.email
