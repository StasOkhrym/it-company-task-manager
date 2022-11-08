from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, "Urgent"),
        (2, "High"),
        (3, "Medium"),
        (4, "Low"),
    ]
    name = models.CharField(max_length=65)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, default="medium"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["priority"]

    def __str__(self) -> str:
        return f"{self.name} (Priority: {self.priority})"
