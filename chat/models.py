from typing import Iterable, Optional
from django.db import models
from django.utils import timezone
from chat.managers import ThreadManager


class TrackingModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(TrackingModel):
    THREAD_TYPE = (("personal", "Personal"), ("group", "Group"))

    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default="group")
    users = models.ManyToManyField("auth_and_reg.CustomUser")

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == "personal" and self.users.count() == 2:
            return f"{self.users.first()} and {self.users.last()}"
        return f"{self.name}"


class Message(TrackingModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey("auth_and_reg.CustomUser", on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"From <Thread - {self.thread}>"

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        super().save(force_insert, force_update, using, update_fields)
        thread = self.thread
        thread.updated = timezone.now()
        thread.save()
