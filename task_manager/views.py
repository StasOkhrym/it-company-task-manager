from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import generic

from task_manager.forms import TaskSearchForm, WorkerSearchForm
from task_manager.models import Worker, Task


def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    deadlines = [(task.deadline - datetime.now().date()).days for task in Task.objects.all()]
    expired_tasks = len(list(filter(lambda a: a < 0, deadlines)))
    closest_deadline = min(filter(lambda a: a >= 0, deadlines))

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "closest_deadline": closest_deadline,
        "expired_tasks": expired_tasks,
        "num_visits": num_visits,
    }

    return render(request, "task_manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    queryset = Task.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:task-detail", kwargs={"pk": self.object.pk}
        )


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = Worker.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        search = self.request.GET.get("search", "")

        context["search_form"] = WorkerSearchForm(initial={"search": search})
        return context

    def get_queryset(self):
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                Q(first_name__icontains=form.cleaned_data["search"]) |
                Q(first_name__icontains=form.cleaned_data["search"]) |
                Q(username__icontains=form.cleaned_data["search"])
            )


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all()


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


@login_required
def toggle_task_assign(request, pk):
    worker = Worker.objects.get(id=request.user.id)
    if (
        Task.objects.get(id=pk) in worker.tasks.all()
    ):
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("task_manager:task-detail", args=[pk]))
