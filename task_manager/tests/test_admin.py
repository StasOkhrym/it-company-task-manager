from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.test_position = Position.objects.create(name="test")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user", password="admin1234", position=self.test_position
        )
        self.client.force_login(self.admin_user)

        self.worker = get_user_model().objects.create_user(
            username="test_driver", password="test12345", position=self.test_position
        )

    def test_worker_position_listed(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_worker_detailed_position_listed(self):
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_position_in_driver_add(self):
        url = reverse("admin:task_manager_worker_add")
        response = self.client.get(url)

        self.assertContains(response, "position")
