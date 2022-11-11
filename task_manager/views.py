from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import generic

from task_manager.forms import (
    TaskSearchForm,
    WorkerSearchForm,
    PositionSearchForm,
    TaskTypeSearchForm,
    WorkerTaskFilterForm,
    TaskForm,
    WorkerCreateForm,
    WorkerUpdateForm,
)
from task_manager.models import Worker, Task, Position, TaskType


def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    deadlines = [
        (task.deadline - datetime.now().date()).days for task in Task.objects.all()
    ]

    expired_tasks = len([deadline for deadline in deadlines if deadline < 0])
    try:
        closest_deadline = sorted([deadline for deadline in deadlines if deadline >= 0])[0]
    except IndexError:
        closest_deadline = -1

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
    queryset = Task.objects.select_related("task_type")
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        not_completed = self.request.GET.get("not_completed", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name, "not_completed": not_completed}
        )
        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data["not_completed"]:
                return self.queryset.filter(
                    name__icontains=form.cleaned_data["name"], is_completed=False
                )
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task_manager:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
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
                Q(first_name__icontains=form.cleaned_data["search"])
                | Q(first_name__icontains=form.cleaned_data["search"])
                | Q(username__icontains=form.cleaned_data["search"])
            )


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)

        not_completed = self.request.GET.get("not_completed", "")

        worker = Worker.objects.get(id=self.kwargs["pk"])
        if not_completed:
            context["task_list"] = worker.tasks.filter(is_completed=False)
        else:
            context["task_list"] = worker.tasks.all()

        context["search_form"] = WorkerTaskFilterForm(
            initial={"not_completed": not_completed}
        )

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm

    def get_success_url(self):
        return reverse_lazy("task_manager:worker-detail", args=[self.object.pk])


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse_lazy("task_manager:worker-detail", args=[self.object.pk])


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5
    queryset = Position.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])

        return self.queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task_manager:position-detail", args=[self.object.pk])


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task_manager:position-detail", args=[self.object.pk])


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    queryset = TaskType.objects.all()
    context_object_name = "task_type_list"
    template_name = "task_manager/task_type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TaskTypeSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])

        return self.queryset


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    context_object_name = "task_type"
    template_name = "task_manager/task_type_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeDetailView, self).get_context_data(**kwargs)

        task_type = TaskType.objects.get(id=self.kwargs["pk"])
        tasks = Task.objects.filter(task_type_id=task_type.id)
        context["tasks"] = tasks

        return context


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    context_object_name = "task_type"
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task_manager:task-type-detail", args=[self.object.pk])


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    context_object_name = "task_type"
    queryset = TaskType.objects.select_related("task")
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task_manager:task-type-detail", args=[self.object.pk])


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    context_object_name = "task_type"
    success_url = reverse_lazy("task_manager:task-type-list")


@login_required
def toggle_task_assign(request, pk):
    worker = Worker.objects.get(id=request.user.id)
    if Task.objects.get(id=pk) in worker.tasks.all():
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("task_manager:task-detail", args=[pk]))


@login_required
def toggle_task_state(request, pk):
    task = Task.objects.get(id=pk)
    if not task.is_completed:
        task.is_completed = True
    else:
        task.is_completed = False
    task.save()
    return HttpResponseRedirect(reverse_lazy("task_manager:task-detail", args=[pk]))
