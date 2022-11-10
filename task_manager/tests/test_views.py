import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType, Position, Worker, Task


class PublicTests(TestCase):
    def test_login(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateTests(TestCase):
    def setUp(self) -> None:
        Position.objects.create(name="test")
        Position.objects.create(name="test1")
        TaskType.objects.create(name="test")
        TaskType.objects.create(name="test1")
        self.user = get_user_model().objects.create_user(
            username="test_user", password="1qazcde3", position_id=1
        )
        Task.objects.create(
            name="test",
            description="test",
            deadline=datetime.datetime.now(),
            is_completed=False,
            priority=3,
            task_type_id=1,
        )
        self.client.force_login(self.user)

    def test_task_type_list(self):
        response = self.client.get(reverse("task_manager:task-type-list"))
        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types),
        )
        self.assertTemplateUsed(response, "task_manager/task_type_list.html")

    def test_task_type_detail(self):
        response = self.client.get(reverse("task_manager:task-type-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_type_detail.html")

    def test_task_list(self):
        response = self.client.get(reverse("task_manager:task-list"))
        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks),
        )
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_task_detail(self):
        response = self.client.get(reverse("task_manager:task-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_detail.html")

    def test_position_list(self):
        response = self.client.get(reverse("task_manager:position-list"))
        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions),
        )
        self.assertTemplateUsed(response, "task_manager/position_list.html")

    def test_position_detail(self):
        response = self.client.get(reverse("task_manager:position-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/position_detail.html")

    def test_worker_list(self):
        response = self.client.get(reverse("task_manager:worker-list"))
        workers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers),
        )
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_worker_detail(self):
        response = self.client.get(reverse("task_manager:worker-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/worker_detail.html")
