from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import random
import os
import requests


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):

        print("-> {}".format(password))
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            phone = phone
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password = password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, passowrd=None, **extra_data):
        print("<- {}".format(extra_data))
        user = self.create_user(
            phone,
            password=extra_data["password"],
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    phone_regex = RegexValidator(regex = r'^[7-9][0-9]{9}$')
    phone = models.CharField(validators = [phone_regex], max_length = 15, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    first_login = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



class PhoneOTP(models.Model):

    phone_regex = RegexValidator(regex = r'^[7-9][0-9]{9}$')
    phone = models.CharField(validators = [phone_regex], max_length = 15, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    validated = models.BooleanField(default=False, help_text='True if OTP is verified')
    # logged = models.BooleanField(default=False, help_text='If OTP Successful')
    # forgot = models.BooleanField(default=False, help_text='Only True for forgot password')
    # forgot_logged = models.BooleanField(default=False, help_text='Only True if validate otp for forgot password is successful ')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)