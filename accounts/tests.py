from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class PermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data")

    def test_student_cannot_access_user_management(self):
        user = User.objects.get(username="ntnhat")
        self.client.force_login(user)
        response = self.client.get(reverse("accounts:user_list"))
        self.assertIn(response.status_code, [302, 403])

# Create your tests here.
