# QR PUBLIC FLOW

## 1. Luồng public verification

Sau khi credential được publish:

1. hệ thống tạo `public_slug`
2. tạo QR code chứa URL:
   - `/xac-thuc/tra-cuu/<public_slug>/`
3. QR được nhúng vào PDF
4. bên thứ ba quét QR hoặc nhập verification code
5. public portal hiển thị:
   - loại credential
   - người sở hữu
   - đơn vị cấp
   - serial number
   - verification code
   - fingerprint hash rút gọn
   - trạng thái signature
   - trạng thái ledger
   - trạng thái `VALID / REVOKED / SUPERSEDED`

## 2. Cách demo QR/public flow

1. Đăng nhập nội bộ
2. Mở chi tiết một credential đã `PUBLISHED`
3. Bấm link `Mở trang verify` hoặc tải PDF
4. Dùng QR hiển thị trong trang chi tiết/PDF
5. Mở public page và quan sát trạng thái

## 3. Các case nên trình diễn

- Case 1: credential hợp lệ
  - signature valid
  - ledger valid
  - status `VALID`

- Case 2: credential bị thu hồi
  - status `REVOKED`
  - hiển thị public note

- Case 3: credential bị thay thế
  - status `SUPERSEDED`
  - có link sang bản mới

## 4. Endpoint liên quan

- public search: `/xac-thuc/`
- public detail by slug: `/xac-thuc/tra-cuu/<slug>/`
- API lookup: `/api/verification/lookup/?value=<code>`
