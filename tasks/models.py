from django.db import models
from users.models import User


class Task(models.Model):
    class Statuses(models.TextChoices):
        ON_HOLD = "ON HOLD", "On hold"
        IN_PROCESS = "IN PROCESS", "In Process"
        COMPLETED = "COMPLETED", "Completed"

    title = models.CharField(max_length=128, unique=True)
    report = models.TextField(null=True, blank=True)
    status = models.CharField(choices=Statuses.choices, default=Statuses.ON_HOLD)
    client = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='client')
    worker = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.SET_NULL, related_name='worker')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'task: {self.title}, client: {self.client}'

