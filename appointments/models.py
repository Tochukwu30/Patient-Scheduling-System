from email.policy import default
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from auth_and_reg.models import Doctor, Patient, CustomUser

# Create your models here.
class Appointment(models.Model):
    "Model of appointments between doctors and patients"

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", _("scheduled")
        CONFIRMED = "confirmed", _("confirmed")
        CANCELLED = "cancelled", _("cancelled")

    created_by = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    patient = models.ForeignKey(Patient, on_delete=models.RESTRICT)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    description = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    scheduled_on = models.DateTimeField(default=timezone.now)
    confirmed_on = models.DateTimeField(null=True, blank=True)
    cancelled_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Appointment between {self.doctor} and {self.patient}"
