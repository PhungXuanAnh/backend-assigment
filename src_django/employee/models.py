from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    ACTIVE = "active"
    NOT_STARTED = "not_started"
    TERMINATED = "terminated"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (NOT_STARTED, "Not started"),
        (TERMINATED, "Terminated"),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    contact_info = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_STARTED)
    auth_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    department = models.ForeignKey(
        "Department", related_name="employees", null=True, on_delete=models.CASCADE
    )
    position = models.ForeignKey(
        "Position", related_name="employees", null=True, on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        "Location", related_name="employees", null=True, on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        "Company", related_name="employees", null=True, on_delete=models.CASCADE
    )


class Company(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    company = models.ForeignKey(
        "Company", related_name="departments", null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name


class DynamicColumn(models.Model):
    company = models.ForeignKey(
        "Company", related_name="dynamic_columns", null=True, on_delete=models.CASCADE
    )
    fields = models.CharField(max_length=100)
