# ARCHITECTURE

## 1. Kiến trúc tổng thể

Hệ thống được thiết kế theo mô hình `Django monolith modular`:

- server-rendered dashboard cho nghiệp vụ nội bộ
- REST API cho truy cập có cấu trúc
- `permissioned blockchain-inspired ledger` cho sự kiện quan trọng
- service layer tách riêng business logic khỏi view
- public verification portal đọc dữ liệu đã được kiểm soát exposure

Luồng chính:

1. `students + academics` cung cấp dữ liệu điều kiện
2. `issuance` tạo hồ sơ cấp phát
3. `policy_engine` evaluate rule kiểu smart contract
4. `issuance` xử lý approval multi-party
5. `credentials` issue PDF + QR + hash + signature
6. `ledger` commit immutable event chain
7. `public_portal + verification` cho tra cứu công khai
8. `audit + reports` phục vụ kiểm toán và báo cáo

## 2. Permissioned blockchain-inspired design

Thay vì blockchain public như Bitcoin, dự án dùng mô hình phù hợp đại học:

- participants được ủy quyền rõ ràng
- chỉ một số role/organization có quyền ghi ledger hay approve
- approval multi-step mô phỏng consensus / endorsement
- public verification được mở có kiểm soát
- không cần token/currency native

Các logical validators:

- Faculty Admin / Department Officer: đề xuất hồ sơ
- Examination / University Admin: xác nhận dữ liệu học vụ và tài chính
- Auditor: xác nhận kiểm soát / discipline
- Registrar: phê duyệt cuối và phát hành
- Signer: ký số chứng chỉ

## 3. Ledger subsystem

`ledger.services.commit_ledger_event()` ghi event append-only với:

- `sequence_no`
- `event_type`
- `entity_type`
- `entity_id`
- `actor_user`
- `actor_organization`
- `payload_json` canonicalized
- `previous_hash`
- `current_hash`

Công thức hash:

`SHA-256(sequence_no + timestamp + event_type + entity_type + entity_id + actor identifiers + canonical payload JSON + previous_hash)`

`ledger.services.verify_ledger_chain()` duyệt lại toàn bộ chain để phát hiện:

- `previous_hash_mismatch`
- `current_hash_mismatch`

## 4. Policy engine

`policy_engine` là lớp `smart-contract-like automation`:

- agreed rules được lưu trong `PolicyRule.expression_json`
- service `evaluate_eligibility_rules()` đọc rule và context từ `student/program/request`
- nếu điều kiện đạt, request được đẩy sang trạng thái đủ điều kiện
- nếu fail, request giữ ở trạng thái review và được ghi ledger + audit

Supported operators hiện tại:

- `eq`
- `gte`
- `lte`
- `gt`
- `lt`
- `in`

## 5. Credential lifecycle

Lifecycle chuẩn:

1. Tạo `IssuanceRequest`
2. Chạy policy evaluation
3. Approval workflow nhiều bước
4. Issue credential record
5. Tạo payload hash
6. Render PDF thật
7. Tạo QR verification
8. Ký số RSA
9. Publish public record
10. Revoke hoặc supersede nếu có thay đổi

## 6. Security và privacy

- custom `AUTH_USER_MODEL`
- role-based access control tại UI và API
- CSRF protection mặc định của Django
- secret/key lấy từ env hoặc file path, không hard-code private key trong code
- public page chỉ lộ dữ liệu tối thiểu
- `mask_value()` dùng để che bớt mã sinh viên ở public view
- audit log và ledger ghi lại hành động quan trọng

## 7. Production-minded settings

- `DATABASE_URL` để chuyển SQLite sang PostgreSQL
- `WhiteNoise` cho static file
- `gunicorn` trong Docker/runtime production
- `DEBUG=False`, secure cookie và HSTS khi chạy production

## 8. Thư mục chính

- `config/`: settings, urls, api router
- `templates/`: giao diện nội bộ + public portal
- `static/`: CSS dashboard
- `media/`: PDF, QR, key file, exported artifacts
