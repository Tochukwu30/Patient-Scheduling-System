from dataclasses import field
from django.contrib import admin
from .models import CustomUser, Doctor, Patient

# Register your models here.
# @admin.register(CustomUser)
# class RequestDemoAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in CustomUser._meta.get_fields()]


admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(Patient)
