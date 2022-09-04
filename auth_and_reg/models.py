import email
from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from auth_and_reg.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model"""

    class Role(models.TextChoices):
        PATIENT = "Patient", _("Patient")
        DOCTOR = "Doctor", _("Doctor")

    email = models.EmailField(
        verbose_name=_("Email address"),
        unique=True,
    )
    role = models.CharField(
        max_length=8,
        choices=Role.choices,
        default=Role.PATIENT,
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        # change the default verbose name of the model
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        if self.role == "Doctor":
            doctor, created = Doctor.objects.get_or_create(
                id=self,
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
            )
            # Returns (object, created). Created is true if the object was created.
            if created:

                doctor.save()
        elif self.role == "Patient":
            patient, created = Patient.objects.get_or_create(
                id=self,
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
            )
            if created:
                patient.save()


class Doctor(models.Model):
    id = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    phone_no = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=100, null=True, unique=True)
    speciality = models.CharField(max_length=100, null=True)
    home_address = models.CharField(max_length=200, null=True)
    office_address = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super(Doctor, self).save(*args, **kwargs)
        user = CustomUser.objects.get(id=self.id.id)
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.save()


class Patient(models.Model):
    id = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    phone_no = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=100, null=True, unique=True)
    home_address = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user = CustomUser.objects.get(id=self.id.id)
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.save()
