from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from core.signing import generate_rsa_key_pair
from credentials.models import SigningKey
from organizations.models import Organization


class Command(BaseCommand):
    help = "Generate RSA sample signing key and register it in the database."

    def add_arguments(self, parser):
        parser.add_argument("--organization-code", default="REG")
        parser.add_argument("--key-name", default="Demo Registrar Key")
        parser.add_argument("--path", default="media/keys/demo_registrar_private.pem")
        parser.add_argument("--force", action="store_true")

    def handle(self, *args, **options):
        organization = Organization.objects.filter(code=options["organization_code"]).first()
        if not organization:
            raise CommandError("Organization not found. Seed organizations first.")

        private_path = Path(options["path"])
        if private_path.exists() and not options["force"]:
            self.stdout.write(self.style.WARNING(f"Private key already exists at {private_path}"))
            key = SigningKey.objects.filter(
                organization=organization,
                key_name=options["key_name"],
            ).first()
            if key:
                self.stdout.write(self.style.SUCCESS(f"Signing key already registered: {key.key_name}"))
                return

        public_key_pem = generate_rsa_key_pair(str(private_path))
        signing_key, _ = SigningKey.objects.update_or_create(
            organization=organization,
            key_name=options["key_name"],
            defaults={
                "algorithm": "RSA",
                "public_key_pem": public_key_pem,
                "private_key_reference": str(private_path),
                "active": True,
            },
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Sample signing key ready: {signing_key.key_name} ({organization.name})"
            )
        )
