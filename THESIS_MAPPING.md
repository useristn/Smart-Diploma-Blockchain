# THESIS 6 CHAPTER MAPPING

## Chương 1: Good Ledger, ownership, timestamp, transaction description

Ứng dụng coi quá trình cấp phát chứng chỉ là một bài toán ledger:

- mỗi thay đổi trạng thái đều thành `LedgerEvent`
- có actor, thời điểm, entity và payload
- ledger không overwrite bản cũ mà append-only
- credential lifecycle được nhìn như transaction pipeline thay vì CRUD đơn thuần

Thành phần liên quan:

- `ledger.models.LedgerEvent`
- `ledger.services.commit_ledger_event`
- `issuance`, `credentials`, `verification`

## Chương 2: Hash, digital signature, append-only logs

Các kỹ thuật mật mã được dùng:

- SHA-256 cho payload hash và PDF hash
- canonical JSON trước khi băm
- RSA application-level digital signature
- append-only hash-chain với `previous_hash/current_hash`
- verify lại signature, payload, PDF, ledger

Thành phần liên quan:

- `core.utils.canonicalize_json`
- `credentials.services.compute_payload_hash`
- `credentials.services.compute_pdf_hash`
- `core.signing`
- `ledger.services.verify_ledger_chain`

## Chương 3: Consensus thinking, validators, permissioned governance

Hệ thống không làm public blockchain mà mô phỏng `permissioned network` trong đại học:

- Faculty/Admin đề xuất hồ sơ
- Examination/University Admin xác nhận
- Auditor kiểm soát
- Registrar phê duyệt cuối
- Signer ký phát hành

Approval workflow nhiều bước đóng vai trò endorsement / consensus logic.

## Chương 4: Transaction processing

Từng hành động quan trọng được tách thành transaction/event:

- tạo issuance request
- eligibility pass/fail
- approval granted/rejected
- credential issued
- PDF rendered
- credential signed
- credential published
- credential verified
- credential revoked
- credential superseded

Điều này thể hiện rõ pipeline `create -> validate -> approve -> commit -> publish`.

## Chương 5: Smart-contract-like rule engine

`policy_engine` là lớp tự động hóa kiểu smart contract:

- rule được định nghĩa sẵn trong `expression_json`
- trigger khi người dùng bấm evaluate
- hệ thống tự đọc context `student/program/request`
- if/then logic quyết định pass/fail
- kết quả được ghi vào DB, audit và ledger

## Chương 6: Permissioned architecture, digital IDs, privacy, governance

Đồ án chọn đúng hướng phù hợp cho bằng cấp số:

- private / permissioned blockchain-inspired
- authorized participants
- limited write access
- public verifiability có kiểm soát
- không cần native currency
- privacy-aware exposure tại public page
- mở rộng được cho tích hợp tiếp theo

Các thách thức và cách xử lý trong thiết kế:

- scalability: monolith modular + PostgreSQL
- privacy: masking dữ liệu public
- security: RBAC, signature, env config, audit
- interoperability: REST API + canonical JSON
- governance: multi-organization approval
