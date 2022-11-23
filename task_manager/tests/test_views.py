from django.contrib.auth import get_user_model
from django.db.models.functions import datetime
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType, Position, Task


class PublicTests(TestCase):
    def test_login_required(self):
        response_login = self.client.get(reverse("login"))
        response_task_type = self.client.get(reverse("task_manager:task-type-list"))
        response_worker = self.client.get(reverse("task_manager:worker-list"))
        response_task = self.client.get(reverse("task_manager:task-list"))
        response_position = self.client.get(reverse("task_manager:position-list"))

        self.assertEqual(response_login.status_code, 200)
        self.assertNotEqual(response_task_type.status_code, 200)
        self.assertNotEqual(response_worker.status_code, 200)
        self.assertNotEqual(response_task.status_code, 200)
        self.assertNotEqual(response_position.status_code, 200)
        self.assertTemplateUsed("registration/login.html")

    def test_login_page(self):
        get_user_model().objects.create_user(
            username="TEST.user",
            password="1qazcded3"
        )

        form_data = {
            "username": "TEST.user",
            "password": "1qazcded3"
        }
        response = self.client.post(reverse("login"), data=form_data)

        self.assertTemplateUsed("registration/login.html")
        self.assertRedirects(response, "/")
        self.assertEqual(response.status_code, 302)


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

    def test_create_worker(self):
        form_data = {
            "username": "test.user",
            "first_name": "Test Name",
            "last_name": "Test Surname",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        self.client.post(reverse("task_manager:worker-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertTemplateUsed("task_manager/worker_form.html")
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])

    def test_update_worker(self):
        get_user_model().objects.create_user(
            username="TEST.user",
            password="1qazcded3"
        )
        form_data = {
            "username": "test.user",
            "first_name": "Test Name",
            "last_name": "Test Surname",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        self.client.post(reverse("task_manager:worker-update", args=[2]), data=form_data)
        updated_user = get_user_model().objects.get(id=2)

        self.assertTemplateUsed("task_manager/worker_form.html")
        self.assertEqual(updated_user.first_name, form_data["first_name"])
        self.assertEqual(updated_user.last_name, form_data["last_name"])