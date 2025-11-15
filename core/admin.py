from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AleraUser, BloodGlucose, PatternAlert
from django.contrib.auth.admin import UserAdmin

admin.site.register(AleraUser, UserAdmin)
admin.site.register(BloodGlucose)
admin.site.register(PatternAlert)
