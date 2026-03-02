from django.db import models
from datetime import date


class Entry(models.Model):
    company_name = models.CharField(max_length=255)
    jobtitle = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)

    APPLICATION_CHOICES = [
        ("email", "Email"),
        ("homepage", "Homepage"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("applied", "Applied"),
        ("rejected", "Rejected"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    status_date = models.DateField(default=date.today)
