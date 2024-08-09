# DJANGO DECLARATIONS
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F, Max, Min
from django.contrib.auth.models import AbstractUser
from django.db.models.query_utils import Q
from django.db import connection
from django.utils import timezone
#GENERAL DECLARATIONS
from datetime import date, datetime
import pandas as pd

#APP DECLARATIONS
import app.m00_common as m00

USER_ROLES = [
    ('Administrator', 'Administrator')
]

# DECLARING CLASSES

class CustomUser(AbstractUser):
    # This is an override of the Django built-in User Model

    def save(self, *args, **kwargs):
        # Your custom save logic
        # ...
        super().save(*args, **kwargs)  # Call the original save() method


class Product(models.Model):
    """
    Here we store all subjects of quiz questions
    """
    name = models.CharField(
        max_length=300, null=True, blank=True)
    barcode = models.CharField(
        max_length=300, null=True, blank=True)
    link = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.barcode


class UserProfile(models.Model):
    # This is a table where we store additional info for each user, like username, birthday
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    username = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    role = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        choices=USER_ROLES)
    last_login = models.DateTimeField(blank=True, null=True)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    

class AccessLog(models.Model):
    """
    Here we store the log of login for each user
    """
    user = models.ForeignKey(
        CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)
    target = models.CharField(
        max_length=300, null=False, blank=False)
    target_id = models.IntegerField()

    def __str__(self):
        return f"User {self.user} accessed {self.target} with ID {self.target_id} in {self.creation}"


class LogingLog(models.Model):
    """
    Here we store the log of accessing subjects, modules, and topics
    """
    user = models.ForeignKey(
        CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    time = models.DateTimeField()