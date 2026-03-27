# TESTING

## 1. Chạy test suite

```bash
python manage.py test
```

Test suite hiện có 17 test tự động, bao phủ các luồng:

- tạo issuance request
- rule evaluation pass
- rule evaluation fail
- approval workflow đúng
- không publish khi chưa sign
- ký chứng chỉ thành công
- verify signature thành công
- verify signature fail khi payload bị đổi
- PDF hash verify đúng
- ledger chain pass
- ledger chain fail khi dữ liệu bị tamper
- public verification trả về `VALID`
- public verification trả về `REVOKED`
- public verification hiển thị bản superseded
- permission cơ bản cho user management

## 2. Kiểm tra nhanh hệ thống

```bash
python manage.py check
python manage.py verify_ledger
```

## 3. Tái tạo dữ liệu demo trước khi test tay

```bash
python manage.py seed_demo_data --reset
```

## 4. Kiểm thử thủ công gợi ý

1. Đăng nhập bằng `faculty`
2. Tạo issuance request mới cho sinh viên đủ điều kiện
3. Chạy `rule evaluation`
4. Duyệt các bước approval
5. Issue credential
6. Đăng nhập bằng `signer` để ký
7. Đăng nhập bằng `registrar` để publish
8. Mở public portal để verify
9. Thử revoke hoặc supersede
10. Mở ledger explorer và verify chain
