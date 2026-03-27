# API REFERENCE

Base URL: `/api/`

## Authentication

Hệ thống hỗ trợ 3 phương thức xác thực:

### JWT Token (khuyến nghị)

Lấy token:

```
POST /api/auth/token/
Content-Type: application/json

{"username": "admin", "password": "admin12345"}
```

Response:

```json
{
  "access": "eyJ0eXAi...",
  "refresh": "eyJ0eXAi..."
}
```

Sử dụng token:

```
Authorization: Bearer <access_token>
```

Refresh token:

```
POST /api/auth/token/refresh/
Content-Type: application/json

{"refresh": "<refresh_token>"}
```

### Session auth

Đăng nhập qua trình duyệt tại `/tai-khoan/dang-nhap/`.

### Basic auth

Dùng `Authorization: Basic <base64(username:password)>`.

## Rate Limiting

- Anonymous: 30 requests/phút
- Authenticated: 120 requests/phút
- Public verification: 60 requests/phút

Khi vượt giới hạn, API trả về `429 Too Many Requests`.

## Phân trang

Response dùng format:

- `count`
- `page`
- `num_pages`
- `next`
- `previous`
- `results`

## 1. Users

- `GET /api/users/`
- `POST /api/users/`
- `GET /api/users/{id}/`
- `PATCH /api/users/{id}/`

## 2. Memberships

- `GET /api/memberships/`
- `POST /api/memberships/`

## 3. Organizations

- `GET /api/organizations/`
- `POST /api/organizations/`
- `GET /api/organizations/{id}/`

## 4. Programs and Courses

- `GET /api/programs/`
- `POST /api/programs/`
- `GET /api/courses/`
- `POST /api/courses/`

## 5. Students

- `GET /api/students/`
- `POST /api/students/`
- `GET /api/student-course-records/`
- `POST /api/student-course-records/`

## 6. Issuance Workflow

- `GET /api/issuance-requests/`
- `POST /api/issuance-requests/`
- `GET /api/approvals/`
- `POST /api/approvals/`

## 7. Credentials

- `GET /api/credentials/`
- `POST /api/credentials/`
- `GET /api/credential-types/`
- `POST /api/credential-types/`

## 8. Policy Engine

- `GET /api/policy-rules/`
- `POST /api/policy-rules/`
- `GET /api/policy-evaluations/`

## 9. Ledger and Audit

- `GET /api/ledger-events/`
- `GET /api/audit-logs/`

## 10. Verification

- `GET /api/verification/lookup/?value=<code-or-slug>`

Response:

```json
{
  "credential_code": "CRD-XXXXXX",
  "verification_code": "VER-XXXXXX",
  "status": "VALID",
  "owner_name": "Nguyễn Văn A",
  "issuer_name": "Văn phòng Registrar",
  "signature_valid": true,
  "ledger_valid": true
}
```

## 11. Reports

- `GET /api/reports/summary/`

## 12. Error handling

- `400`: validation/input error
- `403`: permission denied
- `404`: object not found
- `429`: rate limit exceeded
