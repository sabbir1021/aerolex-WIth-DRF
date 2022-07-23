from django.db import models

USER_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff')
        )
USER_TYPE_CHOICES = (
        ('country_agent', 'Country Agent'),
        ('local_agent', 'Local Agent')
        )
USER_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
        )