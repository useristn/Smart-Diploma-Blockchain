# Hệ thống Quản lý Văn bằng số - HCMUTE

Hệ thống Django full-stack phục vụ đồ án:

`Xây dựng hệ thống cấp phát và xác thực chứng chỉ số / bằng cấp số cho sinh viên ứng dụng công nghệ blockchain`

Ứng dụng mô phỏng kiến trúc `permissioned blockchain-inspired` cho môi trường đại học: có role-based access control, workflow phê duyệt nhiều bước, tamper-evident ledger, ký số ở mức ứng dụng, render PDF thật, QR verification, public verification portal, revoke/supersede, audit log, báo cáo và REST API.

## Công nghệ

- Backend: Django 5 + Django REST Framework
- Frontend: Django Templates + Bootstrap 5
- Database: SQLite mặc định, PostgreSQL qua `DATABASE_URL`
- Signature: RSA với `cryptography`
- PDF: `reportlab`
- QR: `qrcode`
- Static/media: WhiteNoise + Django media storage

## App domain

- `accounts`: custom user, membership, role-based access
- `organizations`: đơn vị trong mạng permissioned
- `academics`: chương trình đào tạo, học phần
- `students`: hồ sơ sinh viên, transcript
- `issuance`: hồ sơ cấp phát và approval workflow
- `policy_engine`: smart-contract-like rule engine
- `credentials`: issue, sign, publish, revoke, supersede, PDF, QR
- `ledger`: append-only tamper-evident event chain
- `verification`: verification service + logs
- `audit`: audit log
- `reports`: thống kê, export
- `public_portal`: cổng xác thực công khai
- `documents`: file đính kèm

## Chức năng chính

- Đăng nhập, hồ sơ người dùng, quản lý user và membership
- Quản lý tổ chức, chương trình đào tạo, học phần, sinh viên
- Tạo issuance request, evaluate policy rules, approval workflow nhiều bước
- Sinh credential payload, render PDF, băm SHA-256, ký số RSA
- Commit các event quan trọng vào ledger hash-chain
- Public verification theo `QR / verification code / credential code / public slug`
- Thu hồi chứng chỉ, đánh dấu superseded và trỏ sang bản mới
- Audit log, ledger explorer, verify chain, dashboard và báo cáo
- REST API cho các domain chính

## Chạy local bằng SQLite

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo_data --reset
python manage.py runserver
```

Mở:

- Dashboard nội bộ: `http://127.0.0.1:8000/dashboard/`
- Cổng xác thực công khai: `http://127.0.0.1:8000/xac-thuc/`
- API root: `http://127.0.0.1:8000/api/`

## Chạy bằng Docker

```bash
copy .env.example .env
docker compose up --build
```

Container web sẽ tự chạy:

- `python manage.py migrate`
- `python manage.py seed_demo_data`
- `python manage.py collectstatic --noinput`
- `gunicorn config.wsgi:application`

## Dữ liệu demo

Tài khoản:

- `admin / admin12345`
- `registrar / registrar12345`
- `faculty / faculty12345`
- `signer / signer12345`
- `auditor / auditor12345`
- `ntnhat / student12345` (Nguyễn Thanh Nhật)
- `nmkhoi / student12345` (Nguyễn Minh Khôi)
- `tdhoa / student12345` (Trần Doãn Hòa)

Kịch bản demo được seed sẵn:

- 1 credential hợp lệ `PUBLISHED`
- 1 credential `REVOKED`
- 1 credential `SUPERSEDED` và có bản mới thay thế
- 1 hồ sơ fail do thiếu tín chỉ/GPA
- 1 hồ sơ fail do `finance_hold`

## Management commands

```bash
python manage.py seed_demo_data --reset
python manage.py verify_ledger
python manage.py generate_sample_keys --organization-code REG --force
python manage.py createsuperuser
python manage.py test
```

## Kiểm thử

Test suite hiện có `17` test integration/service covering:

- tạo issuance request
- rule evaluation pass/fail
- approval workflow
- không publish khi chưa sign
- sign và verify signature
- signature fail khi payload bị đổi
- PDF hash verify
- ledger chain pass/fail
- public verification valid/revoked/superseded
- permission cơ bản

```bash
python manage.py test
```

## Tài liệu

- `ARCHITECTURE.md`
- `API_REFERENCE.md`
- `TESTING.md`
- `DEPLOYMENT.md`
- `THESIS_MAPPING.md`
- `docs/DEMO_SCENARIO.md`
- `docs/QR_PUBLIC_FLOW.md`
