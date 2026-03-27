from django.core.management import call_command
from django.test import TestCase

from ledger.models import LedgerEvent
from ledger.services import verify_ledger_chain


class LedgerIntegrityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data")

    def test_ledger_chain_pass(self):
        report = verify_ledger_chain()
        self.assertTrue(report["ok"])

    def test_ledger_chain_fail_when_data_tampered(self):
        event = LedgerEvent.objects.order_by("sequence_no").first()
        event.payload_json = {"tampered": True}
        event.save(update_fields=["payload_json"])
        report = verify_ledger_chain()
        self.assertFalse(report["ok"])

# Create your tests here.
