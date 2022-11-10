import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import TaskType, Position, Task


class ModelTests(TestCase):
    def test_task_type_str(self):
        name = "TestName"
        task_type = TaskType.objects.create(
            name=name,
        )

        self.assertEqual(str(task_type), name)

    def test_position_str(self):
        name = "TestName"
        position = Position.objects.create(
            name=name,
        )

        self.assertEqual(str(position), name)

    def test_worker_str(self):
        username = "Test1234"
        first_name = "TestName"
        last_name = "TestSurname"
        position = Position.objects.create(name="test")
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            position=position,
        )

        self.assertEqual(str(driver), f"{first_name} {last_name}")

    def test_worker_create(self):
        username = "Test1234"
        password = "TestPass"
        first_name = "TestName"
        last_name = "TestSurname"
        position = Position.objects.create(name="test")
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            position=position,
        )

        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.first_name, first_name)
        self.assertEqual(worker.last_name, last_name)
        self.assertEqual(worker.position, position)

    def test_task_str(self):
        name = ("TestName",)
        description = "test"
        deadline = datetime.datetime.now().date()
        is_completed = False
        priority = 3
        task_type = TaskType.objects.create(name="test")

        task = Task.objects.create(
            name=name,
            description=description,
            deadline=deadline,
            is_completed=is_completed,
            priority=priority,
            task_type=task_type,
        )

        self.assertEqual(str(task), f"{name} (Priority: {priority})")
