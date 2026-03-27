# DEMO SCENARIO

## 1. Mục tiêu demo

Chứng minh hệ thống chạy được end-to-end theo đúng bài toán đồ án:

- hồ sơ cấp phát
- evaluate rule
- approval workflow
- issue PDF
- sign
- publish
- verify công khai
- revoke
- supersede
- verify ledger integrity

## 2. Dữ liệu demo đã có sẵn

Organizations:

- Đại học Demo Blockchain
- Phòng Đào Tạo
- Khoa Công nghệ Thông tin
- Bộ môn Hệ thống thông tin
- Phòng Khảo thí
- Văn phòng Registrar
- Phòng Kiểm định QA

Students:

- Nguyễn Văn A
- Trần Thị B
- Lê Minh C
- Phạm Thị D
- Hoàng Văn E

Credentials:

- 1 bản `PUBLISHED`
- 1 bản `REVOKED`
- 1 bản `SUPERSEDED` + 1 bản thay thế mới

## 3. Kịch bản trình bày

1. Đăng nhập `faculty / faculty12345`
2. Mở `Hồ sơ cấp phát`, tạo một issuance request mới
3. Bấm `Chạy rule evaluation`
4. Duyệt workflow từng bước bằng các tài khoản có role phù hợp
5. Đăng nhập `registrar` để issue credential
6. Đăng nhập `signer` để ký số
7. Đăng nhập `registrar` để publish
8. Mở link public verification hoặc cổng `/xac-thuc/`
9. Dùng một credential seed sẵn để demo `REVOKED`
10. Dùng credential `SUPERSEDED` để demo điều hướng sang bản mới
11. Mở `Ledger Explorer`
12. Chạy `python manage.py verify_ledger`

## 4. Điểm nhấn khi thuyết trình

- mỗi bước quan trọng đều tạo `LedgerEvent`
- approval workflow chính là consensus logic trong môi trường đại học
- rule engine phản ánh tư duy smart contract
- signature + hash + QR + public portal thể hiện tính xác thực công khai
- revoke và supersede cho thấy ledger vẫn giữ lịch sử đầy đủ
