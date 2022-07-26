from django.db import models

# User Create

USER_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff')
        )

USER_TYPE_CHOICES = (
        ('country_user', 'Country User'),
        ('local_user', 'Local User')
        )
USER_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
        )

# Agent

COUNTRY_CHOICES = (
        ('uk','UK'),
        ('bd', 'BD'),
        ('ind', 'IND'),
        ('mal','MAL'),
        ('pk','PK'),
        ('sf','SF'),
        ('usa','USA'),
        ('aus','AUS')
        )

PAYMENT_POLICY_CHOICES = (
        ('credit', 'Credit'),
        ('prepaid', 'Prepaid')
        )

AGENT_TYPE_CHOICES = (
        ('country_agent', 'Country Agent'),
        ('local_agent', 'Local Agent')
        )

# Payment

PAYMENT_TYPE_CHOICES = (
        ('bkash', 'Bkash'),
        ('bank', 'Bank'),
        ('nagad', 'Nagad'),

        )