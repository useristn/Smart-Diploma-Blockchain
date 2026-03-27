# DEPLOYMENT

## 1. Local development

```bash
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo_data --reset
python manage.py runserver
```

## 2. Docker deployment

```bash
copy .env.example .env
docker compose up --build
```

Mặc định `docker-compose.yml` dùng:

- `postgres:16-alpine`
- `gunicorn`
- `DATABASE_URL=postgresql://postgres:postgres@db:5432/credential_ledger`

## 3. Production checklist

- đổi `DJANGO_SECRET_KEY`
- đặt `DJANGO_DEBUG=False`
- cấu hình `DJANGO_ALLOWED_HOSTS`
- cấu hình `DJANGO_CSRF_TRUSTED_ORIGINS`
- dùng PostgreSQL thay cho SQLite
- mount volume cho `media/`
- backup private key file trong `media/keys/`
- chạy `collectstatic`
- bật reverse proxy như Nginx/Caddy nếu triển khai Internet

## 4. Superuser và seed

```bash
python manage.py createsuperuser
python manage.py seed_demo_data --reset
python manage.py generate_sample_keys --organization-code REG --force
python manage.py verify_ledger
```

## 5. Gợi ý triển khai thật

- App server: Gunicorn
- Reverse proxy: Nginx
- DB: PostgreSQL
- Object storage: có thể thay `MEDIA_ROOT` bằng S3/MinIO sau này
- Monitoring: thêm Prometheus/Grafana hoặc Sentry ở giai đoạn tiếp theo
