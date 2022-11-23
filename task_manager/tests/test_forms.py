from django.contrib.auth import get_user_model
from django.db.models.functions import datetime
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, TaskType, Task


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        Position.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234", position_id=1
        )
        self.worker = get_user_model().objects.create_user(
            username="worker.user",
            first_name="TEST",
            last_name="USER",
            password="1qazcde3",
            position_id=1,
        )
        self.client.force_login(self.user)

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

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position, None)

    def test_delete_worker(self):
        response = self.client.post(
            reverse("task_manager:worker-delete", kwargs={"pk": self.worker.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(id=self.worker.id).exists())

    def test_search_worker_form(self):
        get_user_model().objects.create_user(
            username="test.username",
            password="1qazcde3",
        )
        response = self.client.get(reverse("task_manager:worker-list") + "?model=d")
        workers = get_user_model().objects.filter(username__icontains="d")

        self.assertNotEqual(list(response.context["worker_list"]), list(workers))
        self.assertEqual(len(response.context["worker_list"]), 3)
        self.assertEqual(len(workers), 0)


class PositionTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_position(self):
        form_data = {"name": "Narnia"}
        response = self.client.post(
            reverse("task_manager:position-create"), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Position.objects.get(id=1).name, "Narnia")

    def test_update_position(self):
        position = Position.objects.create(name="Doors")
        form_data = {"name": "Not Doors"}
        response = self.client.post(
            reverse("task_manager:position-update", kwargs={"pk": position.id}),
            data=form_data,
        )
        Position.objects.get(id=position.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Position.objects.get(id=position.id).name, "Not Doors")

    def test_delete_position(self):
        position = Position.objects.create(
            name="Doors",
        )
        response = self.client.post(
            reverse("task_manager:position-delete", kwargs={"pk": position.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(id=position.id).exists())

    def test_search_position_form(self):
        Position.objects.create(name="SanYong")
        Position.objects.create(name="TesYong")
        response = self.client.get(reverse("task_manager:position-list") + "?name=a")
        manufacturers = Position.objects.filter(name__icontains="a")

        self.assertEqual(list(response.context["position_list"]), list(manufacturers))
        self.assertEqual(Position.objects.count(), 2)
        self.assertEqual(len(manufacturers), 1)


class TaskTypeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_task_type(self):
        form_data = {"name": "Narnia"}
        response = self.client.post(
            reverse("task_manager:task-type-create"), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskType.objects.get(id=1).name, "Narnia")

    def test_update_task_type(self):
        task_type = TaskType.objects.create(name="Doors")
        form_data = {"name": "Not Doors"}
        response = self.client.post(
            reverse("task_manager:task-type-update", kwargs={"pk": task_type.id}),
            data=form_data,
        )
        TaskType.objects.get(id=task_type.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskType.objects.get(id=task_type.id).name, "Not Doors")

    def test_delete_task_type(self):
        task_type = TaskType.objects.create(
            name="Doors",
        )
        response = self.client.post(
            reverse("task_manager:task-type-delete", kwargs={"pk": task_type.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(id=task_type.id).exists())

    def test_search_task_type_form(self):
        TaskType.objects.create(name="SanYong")
        TaskType.objects.create(name="TesYong")
        response = self.client.get(reverse("task_manager:task-type-list") + "?name=a")
        manufacturers = TaskType.objects.filter(name__icontains="a")

        self.assertEqual(list(response.context["task_type_list"]), list(manufacturers))
        self.assertEqual(TaskType.objects.count(), 2)
        self.assertEqual(len(manufacturers), 1)


class TaskTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="test")

    def test_create_task(self):
        form_data = {
            "name": "TestName",
            "description": "test",
            "deadline": datetime.datetime.now().date(),
            "is_completed": False,
            "priority": 3,
            "task_type": self.task_type.id,
            "assignees": [self.user.id],
        }
        response = self.client.post(reverse("task_manager:task-create"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.get(id=1).name, "TestName")

    def test_update_task(self):
        task = Task.objects.create(
            name="Doors",
            description="Test",
            deadline=datetime.datetime.now().date(),
            is_completed=False,
            priority=3,
            task_type=self.task_type,
        )
        form_data = {
            "name": "TestName",
            "description": "test",
            "deadline": datetime.datetime.now().date(),
            "is_completed": False,
            "priority": 3,
            "task_type": self.task_type.id,
            "assignees": [self.user.id],
        }
        response = self.client.post(
            reverse("task_manager:task-update", kwargs={"pk": task.id}),
            data=form_data,
        )
        Task.objects.get(id=task.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.get(id=task.id).name, "TestName")

    def test_delete_task_type(self):
        task = Task.objects.create(
            name="Doors",
            description="Test",
            deadline=datetime.datetime.now().date(),
            is_completed=False,
            priority=3,
            task_type=self.task_type,
        )
        response = self.client.post(
            reverse("task_manager:task-delete", kwargs={"pk": task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_search_task_form(self):
        Task.objects.create(
            name="Doors",
            description="Test",
            deadline=datetime.datetime.now().date(),
            is_completed=False,
            priority=3,
            task_type=self.task_type,
        )
        Task.objects.create(
            name="Doars",
            description="Test",
            deadline=datetime.datetime.now().date(),
            is_completed=False,
            priority=3,
            task_type=self.task_type,
        )
        response = self.client.get(reverse("task_manager:task-list") + "?name=a")
        tasks = Task.objects.filter(name__icontains="a")

        self.assertEqual(list(response.context["task_list"]), list(tasks))
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(len(tasks), 1)

    def test_toggle_task_assign(self):
        task = Task.objects.create(
            name="Doors",
            description="Test",
            deadline=datetime.datetime.now().date(),
            is_completed=False,
            priority=3,
            task_type=self.task_type,
        )

        response_add = self.client.post(
            reverse("task_manager:toggle-task-assign", kwargs={"pk": self.user.id})
        )
        task.refresh_from_db()
        self.assertEqual(response_add.status_code, 302)
        self.assertEqual(task.assignees.count(), 1)

        response_remove = self.client.post(
            reverse("task_manager:toggle-task-assign", kwargs={"pk": self.user.id})
        )
        task.refresh_from_db()
        self.assertEqual(response_remove.status_code, 302)
        self.assertEqual(task.assignees.count(), 0)

    def test_toggle_task_state(self):
        task = Task.objects.create(
            name="Doors",
            description="Test",
            deadline=datetime.datetime.now().date(),
            is_completed=False,
            priority=3,
            task_type=self.task_type,
        )

        response_add = self.client.post(
            reverse("task_manager:toggle-task-state", kwargs={"pk": task.id})
        )
        task.refresh_from_db()
        self.assertEqual(response_add.status_code, 302)
        self.assertEqual(task.is_completed, True)

        response_remove = self.client.post(
            reverse("task_manager:toggle-task-state", kwargs={"pk": task.id})
        )
        task.refresh_from_db()
        self.assertEqual(response_remove.status_code, 302)
        self.assertEqual(task.is_completed, False)
