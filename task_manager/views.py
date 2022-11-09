from django.shortcuts import render
from django.utils.datetime_safe import datetime

from task_manager.models import Worker, Task


def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    closest_deadline = min([(task.deadline - datetime.now().date()).days for task in Task.objects.all()])

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "closest_deadline": closest_deadline,
        "num_visits": num_visits,
    }

    return render(request, "task_manager/index.html", context=context)
