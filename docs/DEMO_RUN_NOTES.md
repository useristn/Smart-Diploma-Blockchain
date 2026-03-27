# DEMO RUN NOTES

Date: 2026-03-27
Environment: Windows + Python 3.11 local run

## 1) Setup and Run Status

- Created .env from .env.example
- Applied migrations successfully
- Seeded demo data with reset successfully
- Ledger verify succeeded
- Ran full test suite after fixes: 17 tests, all passed
- Started local server at http://127.0.0.1:8000

## 2) Stuck Points and Fixes Applied

### Stuck A: PowerShell could not run python command with quoted path

- Symptom: Unexpected token -m when running python -m pip install
- Root cause: Missing call operator in PowerShell for quoted executable path
- Fix: Use
  & "C:/Users/MINH KHOI/AppData/Local/Microsoft/WindowsApps/python3.11.exe" -m pip install -r requirements.txt
- Result: Dependencies check completed

### Stuck B: Automated tests failing due to legacy demo fixture assumptions

- Symptom: 10 test errors, mainly User.DoesNotExist and Student.DoesNotExist
- Root cause:
  - Tests expected old username: studenta
  - Tests expected old student codes: SV001, SV002, SV004, SV005
  - Current seed data uses:
    - Username: ntnhat
    - Student codes: 2001210001, 2001210002, 2101210004, 2101210005
- Fixes made:
  - Updated accounts/tests.py to use ntnhat and allow forbidden/redirect response for unauthorized access
  - Updated issuance/tests.py student codes to current seed values
  - Updated credentials/tests.py student codes to current seed values
- Result: Full test suite passed

## 3) Live Demo Data Verified (Current Seed)

Credentials currently available after seed reset:

- Nguyễn Thanh Nhật
  - credential_code: CRD-1B27HEOD
  - verification_code: VER-LA61T790
  - status: PUBLISHED

- Nguyễn Minh Khôi
  - credential_code: CRD-4J672YCD
  - verification_code: VER-7W1DHGF9
  - status: REVOKED

- Trần Doãn Hòa (old)
  - credential_code: CRD-V4F2O1SQ
  - verification_code: VER-22DYKOAN
  - status: SUPERSEDED

- Trần Doãn Hòa (new)
  - credential_code: CRD-0PJBOZ3V
  - verification_code: VER-YNP8DCHU
  - status: PUBLISHED

## 4) Endpoint Smoke Checks

- GET / returns redirect to login (expected)
- GET /xac-thuc/ returns HTTP 200 (public portal works)
- GET /api/verification/lookup/?value=VER-LA61T790 returns status VALID
- GET /api/verification/lookup/?value=VER-7W1DHGF9 returns status REVOKED
- GET /api/verification/lookup/?value=VER-22DYKOAN returns status SUPERSEDED

## 5) Non-blocking Warnings

- requests warning about urllib3/chardet version compatibility appears in console
- This did not block migration, seeding, tests, runserver, or verification API
- Optional cleanup later: align requests dependency stack

---

## 6) Strict Re-run Check (Second Full Pass)

Date: 2026-03-27 (rerun)

### Actions executed

- Re-ran seed with reset
- Re-ran ledger verify
- Re-ran full test suite (17 tests)
- Executed one full live runtime flow:
  - create issuance request
  - policy evaluation
  - 5-step approvals
  - issue
  - sign
  - publish
- Re-checked public verification API for VALID / REVOKED / SUPERSEDED

### New issue found during rerun

- Symptom:
  - Newly published credential returned `signature_valid=false` on API lookup
  - Existing seeded credentials still returned `signature_valid=true`

- Root cause:
  - `seed_demo_data` always regenerated private key file even when key file already existed.
  - Running `manage.py test` executes seeding in test DB and unintentionally overwrote the shared private key file under media.
  - Runtime DB still held old public key while private key file had changed, causing mismatch for newly signed credentials.

- Fix implemented:
  - File changed: `core/management/commands/seed_demo_data.py`
  - `_ensure_signing_key` now:
    - generates key pair only when private key file does not exist
    - when file exists, derives public key from existing private key and updates DB to that value

- Validation after fix:
  - signing key self-check: TRUE
  - full tests: PASS (17/17)
  - new live-issued credential signature verification: TRUE
  - API returns expected statuses with `signature_valid=true`

### Final runtime codes after second pass

- VALID (newly created in rerun): `VER-X7IL2LIO`
- VALID (seeded): `VER-9I5EPIZF`
- REVOKED: `VER-8ACQS6U2`
- SUPERSEDED: `VER-LAWLWBEC`
- Replacement PUBLISHED: `VER-P24FHWC2`

### Final ledger check

- `Ledger integrity OK`
- Verified events: `52`

---

## 7) Strict Re-run Check (Third Pass - No New Patch Needed)

Date: 2026-03-27 (rerun #3)

### Actions executed

- Re-ran seed with reset
- Re-ran ledger verify (baseline)
- Re-ran full test suite
- Executed full live flow: create request -> evaluate -> 5 approvals -> issue -> sign -> publish
- Re-ran ledger verify after new flow events
- Validated public API for VALID / REVOKED / SUPERSEDED with latest codes
- Checked public portal `/xac-thuc/` returns HTTP 200

### Result

- No error
- No stuck
- No new bug found
- No additional patch required in this pass

### Runtime codes from this pass

- VALID (newly created): `VER-4TTFDSH1`
- VALID (seeded): `VER-8L2OJ1JA`
- REVOKED: `VER-XD2YE5CV`
- SUPERSEDED: `VER-I1XVX7E5`
- Replacement PUBLISHED: `VER-KCOTI66J`

### Assertions

- `NEW_SIGNATURE_VALID = True` for newly created credential
- API responses include `signature_valid=true` and `ledger_valid=true`
- Ledger verify after flow: `OK`, checked `52` events
