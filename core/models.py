from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class AleraUser(AbstractUser):
    diabetes_type = models.CharField(max_length=32, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class BloodGlucose(models.Model):
    user = models.ForeignKey(AleraUser, on_delete=models.CASCADE)
    value_mgdl = models.DecimalField(max_digits=6, decimal_places=1)
    timestamp = models.DateTimeField(default=timezone.now)
    meal_tag = models.CharField(max_length=32, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-timestamp"]


class PatternAlert(models.Model):
    user = models.ForeignKey(AleraUser, on_delete=models.CASCADE)
    summary = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
