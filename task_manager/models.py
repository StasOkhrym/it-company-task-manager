from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=65)


class Position(models.Model):
    name = models.CharField(max_length=65)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    name = models.CharField(max_length=65)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
