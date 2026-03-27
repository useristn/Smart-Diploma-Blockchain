from django.core.management.base import BaseCommand

from ledger.services import verify_ledger_chain


class Command(BaseCommand):
    help = "Verify ledger hash-chain integrity."

    def handle(self, *args, **options):
        report = verify_ledger_chain()
        if report["ok"]:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Ledger integrity OK. Checked {report['checked']} events. Last hash: {report['last_hash']}"
                )
            )
        else:
            self.stdout.write(self.style.ERROR("Ledger integrity FAILED."))
            for issue in report["issues"]:
                self.stdout.write(str(issue))
