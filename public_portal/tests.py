from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from credentials.models import Credential


class PublicVerificationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data")

    def test_public_verification_valid_status(self):
        credential = Credential.objects.filter(current_status="PUBLISHED").first()
        response = self.client.get(reverse("public_portal:detail", args=[credential.public_slug]))
        self.assertContains(response, "VALID")

    def test_public_verification_revoked_status(self):
        credential = Credential.objects.filter(current_status="REVOKED").first()
        response = self.client.get(reverse("public_portal:detail", args=[credential.public_slug]))
        self.assertContains(response, "REVOKED")

    def test_superseded_public_page_shows_new_version_link(self):
        credential = Credential.objects.filter(current_status="SUPERSEDED").first()
        response = self.client.get(reverse("public_portal:detail", args=[credential.public_slug]))
        self.assertContains(response, "Mở bản mới")

# Create your tests here.
