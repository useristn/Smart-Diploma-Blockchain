# MANUAL TESTING - Smart Diploma Blockchain

## Mục lục
- [A. Chuẩn bị môi trường](#a-chuẩn-bị-môi-trường)
- [B. Tài khoản demo](#b-tài-khoản-demo)
- [C. Test Cases](#c-test-cases)
  - [TC-01: Đăng nhập & Phân quyền](#tc-01-đăng-nhập--phân-quyền)
  - [TC-02: Quản lý Tổ chức](#tc-02-quản-lý-tổ-chức)
  - [TC-03: Quản lý Chương trình & Môn học](#tc-03-quản-lý-chương-trình--môn-học)
  - [TC-04: Quản lý Sinh viên](#tc-04-quản-lý-sinh-viên)
  - [TC-05: Quy trình Cấp phát (Issuance Workflow)](#tc-05-quy-trình-cấp-phát-issuance-workflow)
  - [TC-06: Policy Engine (Rule Evaluation)](#tc-06-policy-engine-rule-evaluation)
  - [TC-07: Approval Workflow (Consensus)](#tc-07-approval-workflow-consensus)
  - [TC-08: Cấp phát Chứng chỉ (Issue Credential)](#tc-08-cấp-phát-chứng-chỉ-issue-credential)
  - [TC-09: Ký số (Digital Signing)](#tc-09-ký-số-digital-signing)
  - [TC-10: Publish Chứng chỉ](#tc-10-publish-chứng-chỉ)
  - [TC-11: Thu hồi (Revocation)](#tc-11-thu-hồi-revocation)
  - [TC-12: Thay thế (Supersede)](#tc-12-thay-thế-supersede)
  - [TC-13: Batch Issuance & Merkle Tree](#tc-13-batch-issuance--merkle-tree)
  - [TC-14: Xác thực công khai (Public Verification)](#tc-14-xác-thực-công-khai-public-verification)
  - [TC-15: QR Code Verification](#tc-15-qr-code-verification)
  - [TC-16: Ledger Explorer & Chain Integrity](#tc-16-ledger-explorer--chain-integrity)
  - [TC-17: Audit Logging](#tc-17-audit-logging)
  - [TC-18: Reports & Export](#tc-18-reports--export)
  - [TC-19: REST API Testing](#tc-19-rest-api-testing)
  - [TC-20: Student Portal](#tc-20-student-portal)
  - [TC-21: Dashboard](#tc-21-dashboard)
  - [TC-22: Quản lý User & Membership](#tc-22-quản-lý-user--membership)
  - [TC-23: Bảo mật & Access Control](#tc-23-bảo-mật--access-control)
  - [TC-24: Edge Cases & Error Handling](#tc-24-edge-cases--error-handling)
  - [TC-25: Email Notifications](#tc-25-email-notifications)
  - [TC-26: Performance & Rate Limiting](#tc-26-performance--rate-limiting)
- [D. Checklist tổng hợp](#d-checklist-tổng-hợp)

---

## A. Chuẩn bị môi trường

### Bước 1: Khởi tạo database và dữ liệu demo
```bash
python manage.py migrate
python manage.py seed_demo_data --reset
python manage.py generate_sample_keys
```

### Bước 2: Chạy server
```bash
python manage.py runserver
```

### Bước 3: Mở trình duyệt
- URL: `http://127.0.0.1:8000/`
- Chuẩn bị 2 trình duyệt (hoặc 1 trình duyệt thường + 1 incognito) để test nhiều role

---

## B. Tài khoản demo

| Username | Password | Role | Mô tả |
|----------|----------|------|--------|
| admin | admin12345 | SYSTEM_ADMIN | Quản trị toàn hệ thống |
| registrar | registrar12345 | REGISTRAR | Phê duyệt cuối, publish |
| faculty | faculty12345 | FACULTY_ADMIN | Quản lý khoa, duyệt bước academic |
| signer | signer12345 | SIGNER | Ký số chứng chỉ |
| auditor | auditor12345 | AUDITOR | Kiểm toán, duyệt bước discipline |
| studenta | student12345 | STUDENT | Sinh viên Nguyễn Văn A |
| studentb | student12345 | STUDENT | Sinh viên Trần Thị B |

---

## C. Test Cases

---

### TC-01: Đăng nhập & Phân quyền

#### TC-01.1: Đăng nhập thành công
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Truy cập `http://127.0.0.1:8000/` | Redirect đến trang đăng nhập `/tai-khoan/dang-nhap/` | ☐ |
| 2 | Nhập `admin / admin12345`, click Đăng nhập | Redirect đến Dashboard `/dashboard/` | ☐ |
| 3 | Kiểm tra sidebar hiển thị đầy đủ menu | Hiển thị tất cả menu: Tổ chức, Học vụ, Sinh viên, Cấp phát, Chứng chỉ, Sổ cái, Kiểm toán, Báo cáo | ☐ |

#### TC-01.2: Đăng nhập thất bại
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Nhập `admin / sai_password` | Hiển thị thông báo lỗi, không đăng nhập được | ☐ |
| 2 | Nhập `nonexistent / password` | Hiển thị thông báo lỗi | ☐ |
| 3 | Để trống username/password | Hiển thị validation error | ☐ |

#### TC-01.3: Phân quyền theo Role
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `studenta`, truy cập `/tai-khoan/nguoi-dung/` | Bị chặn (403 hoặc redirect), chỉ SYSTEM_ADMIN/UNIVERSITY_ADMIN mới xem được | ☐ |
| 2 | Đăng nhập `studenta`, truy cập `/to-chuc/tao/` | Bị chặn, student không có quyền tạo tổ chức | ☐ |
| 3 | Đăng nhập `faculty`, truy cập `/tai-khoan/nguoi-dung/` | Bị chặn, faculty không phải admin | ☐ |
| 4 | Đăng nhập `admin`, truy cập `/tai-khoan/nguoi-dung/` | Hiển thị danh sách người dùng | ☐ |
| 5 | Đăng nhập `studenta`, truy cập `/sinh-vien/portal/` | Hiển thị Student Portal | ☐ |
| 6 | Đăng nhập `admin`, truy cập `/sinh-vien/portal/` | Redirect về dashboard (không phải student) | ☐ |

#### TC-01.4: Đổi mật khẩu
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập bất kỳ, vào `/tai-khoan/doi-mat-khau/` | Hiển thị form đổi mật khẩu | ☐ |
| 2 | Nhập mật khẩu cũ đúng + mật khẩu mới hợp lệ | Đổi thành công, thông báo success | ☐ |
| 3 | Nhập mật khẩu cũ sai | Hiển thị lỗi | ☐ |

#### TC-01.5: Đăng xuất
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Click Đăng xuất (hoặc truy cập `/tai-khoan/dang-xuat/`) | Redirect về trang đăng nhập | ☐ |
| 2 | Sau khi đăng xuất, truy cập `/dashboard/` | Redirect về trang đăng nhập | ☐ |

---

### TC-02: Quản lý Tổ chức

#### TC-02.1: Xem danh sách tổ chức
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin`, vào `/to-chuc/` | Hiển thị danh sách tổ chức: Đại học Demo, Khoa CNTT, Phòng Đào Tạo, etc. | ☐ |
| 2 | Mỗi tổ chức hiển thị: code, tên, loại, trạng thái | Thông tin đầy đủ, đúng | ☐ |

#### TC-02.2: Tạo tổ chức mới
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin`, vào `/to-chuc/tao/` | Hiển thị form tạo tổ chức | ☐ |
| 2 | Điền: Code=`TEST`, Name=`Khoa Test`, Type=`FACULTY`, Parent=`Đại học Demo` | Form hợp lệ | ☐ |
| 3 | Submit form | Tạo thành công, redirect về detail hoặc list | ☐ |
| 4 | Kiểm tra tổ chức mới xuất hiện trong danh sách | Có trong list | ☐ |

#### TC-02.3: Xem chi tiết tổ chức
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Click vào một tổ chức trong danh sách | Hiển thị detail page | ☐ |
| 2 | Kiểm tra: code, name, type, parent, email, address, các flag | Đúng thông tin | ☐ |

#### TC-02.4: Sửa tổ chức
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào chi tiết → click Sửa | Hiển thị form pre-filled | ☐ |
| 2 | Sửa name, submit | Cập nhật thành công | ☐ |

---

### TC-03: Quản lý Chương trình & Môn học

#### TC-03.1: Xem danh sách chương trình đào tạo
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin` hoặc `faculty`, vào `/hoc-vu/` | Hiển thị danh sách chương trình | ☐ |
| 2 | Kiểm tra có chương trình CNTT demo | Có, hiển thị degree_type, credits, GPA min | ☐ |

#### TC-03.2: Tạo chương trình mới
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin`, tạo chương trình: Code=`KTPM`, Name=`Kỹ thuật Phần mềm`, Degree=`Bachelor`, Credits=`140`, Min GPA=`2.0` | Tạo thành công | ☐ |
| 2 | Chương trình mới xuất hiện trong danh sách | Có | ☐ |

#### TC-03.3: Xem chi tiết chương trình
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Click vào chương trình | Hiển thị detail: thông tin chương trình + danh sách môn học | ☐ |

#### TC-03.4: Tạo môn học
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tạo môn học: Code=`CS101`, Name=`Intro to CS`, Credits=3, Program=CNTT | Tạo thành công | ☐ |
| 2 | Môn học xuất hiện trong danh sách | Có | ☐ |

---

### TC-04: Quản lý Sinh viên

#### TC-04.1: Xem danh sách sinh viên
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin`, vào `/sinh-vien/` | Hiển thị danh sách sinh viên demo (A, B, C, D, E) | ☐ |
| 2 | Mỗi sinh viên hiển thị: MSSV, họ tên, khoa, trạng thái | Thông tin đúng | ☐ |

#### TC-04.2: Tạo sinh viên mới
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào `/sinh-vien/tao/`, điền đầy đủ thông tin | Form hiển thị đúng | ☐ |
| 2 | Điền: MSSV=`SV999`, Name=`Test Student`, DOB, Email, Faculty, Program, GPA=3.5, Credits=140 | Tạo thành công | ☐ |
| 3 | Kiểm tra sinh viên mới trong danh sách | Có | ☐ |

#### TC-04.3: Xem chi tiết sinh viên
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Click vào sinh viên | Hiển thị đầy đủ: thông tin cá nhân, khoa, chương trình, GPA, credits, trạng thái tốt nghiệp, hold flags | ☐ |
| 2 | Kiểm tra danh sách course records | Hiển thị các môn đã học, điểm, passed/failed | ☐ |

#### TC-04.4: Sửa thông tin sinh viên
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào chi tiết → Sửa, thay đổi GPA | Cập nhật thành công | ☐ |
| 2 | Thay đổi finance_hold = True | Cập nhật, sinh viên bị block graduation | ☐ |

#### TC-04.5: Validation sinh viên
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tạo sinh viên với MSSV đã tồn tại | Hiển thị lỗi trùng mã | ☐ |
| 2 | Tạo sinh viên thiếu trường bắt buộc | Hiển thị validation error | ☐ |

---

### TC-05: Quy trình Cấp phát (Issuance Workflow)

> **Đây là test case quan trọng nhất - test toàn bộ luồng end-to-end**

#### TC-05.1: Tạo hồ sơ cấp phát
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `faculty`, vào `/cap-phat/tao/` | Hiển thị form tạo issuance request | ☐ |
| 2 | Chọn: Student=`Nguyễn Văn A`, Credential Type, Template | Form hợp lệ | ☐ |
| 3 | Submit | Tạo thành công, status = `SUBMITTED` | ☐ |
| 4 | Kiểm tra 5 approval steps tự động tạo | ACADEMIC, EXAMINATION, FINANCE, DISCIPLINE, REGISTRAR đều ở PENDING | ☐ |
| 5 | Kiểm tra LedgerEvent mới: `ISSUANCE_REQUEST_CREATED` | Event xuất hiện trong sổ cái | ☐ |

#### TC-05.2: Tạo hồ sơ cho sinh viên không đủ điều kiện
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tạo issuance request cho sinh viên có GPA thấp hoặc finance_hold=True | Tạo được request (chưa evaluate) | ☐ |
| 2 | Chạy evaluate → quy tắc fail | Hiển thị kết quả: FAIL, lý do cụ thể | ☐ |

---

### TC-06: Policy Engine (Rule Evaluation)

#### TC-06.1: Evaluate thành công
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở hồ sơ cấp phát (sinh viên đủ điều kiện) | Detail page hiển thị | ☐ |
| 2 | Click "Chạy đánh giá quy tắc" (hoặc nút tương đương) | Hệ thống chạy tất cả PolicyRule loại ELIGIBILITY | ☐ |
| 3 | Kiểm tra kết quả | Tất cả rules PASS, status chuyển sang `UNDER_REVIEW` hoặc `ACADEMIC_ELIGIBLE` | ☐ |
| 4 | Kiểm tra `evaluation_summary_json` | Hiển thị chi tiết từng rule: tên rule, kết quả, điều kiện | ☐ |
| 5 | Kiểm tra LedgerEvent: `ELIGIBILITY_CHECK_PASSED` | Event xuất hiện | ☐ |

#### TC-06.2: Evaluate thất bại
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tạo request cho sinh viên GPA < min_gpa | Request tạo thành công | ☐ |
| 2 | Chạy evaluate | Kết quả: FAIL cho rule GPA | ☐ |
| 3 | Kiểm tra LedgerEvent: `ELIGIBILITY_CHECK_FAILED` | Event xuất hiện | ☐ |
| 4 | Tạo request cho sinh viên finance_hold=True | Evaluate FAIL cho rule finance | ☐ |
| 5 | Tạo request cho sinh viên credits < total_required_credits | Evaluate FAIL cho rule credits | ☐ |

#### TC-06.3: Xem danh sách Policy Rules
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào `/chinh-sach/` | Danh sách rules hiển thị | ☐ |
| 2 | Click vào rule | Chi tiết: expression_json, type, priority, active | ☐ |
| 3 | Kiểm tra expression_json có dạng AND/OR với conditions | Đúng cấu trúc | ☐ |

---

### TC-07: Approval Workflow (Consensus)

> **Test tuần tự 5 bước phê duyệt - mỗi bước cần đăng nhập đúng role**

#### TC-07.1: Bước 1 - Academic Approval (FACULTY_ADMIN)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `faculty` | Đăng nhập thành công | ☐ |
| 2 | Mở hồ sơ cấp phát đã evaluate PASS | Detail page, step ACADEMIC đang PENDING | ☐ |
| 3 | Click Phê duyệt bước ACADEMIC | Step chuyển APPROVED, ghi lại approved_by, approved_at | ☐ |
| 4 | Kiểm tra LedgerEvent: `APPROVAL_GRANTED` | Event xuất hiện, entity_type=ApprovalStep | ☐ |

#### TC-07.2: Bước 2 - Examination Approval (EXAMINATION_OFFICER)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập tài khoản có role EXAMINATION_OFFICER (hoặc `admin`) | Đăng nhập thành công | ☐ |
| 2 | Mở hồ sơ, click Phê duyệt bước EXAMINATION | Step chuyển APPROVED | ☐ |
| 3 | Kiểm tra LedgerEvent | Event mới xuất hiện | ☐ |

#### TC-07.3: Bước 3 - Finance Approval (UNIVERSITY_ADMIN)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin` (UNIVERSITY_ADMIN hoặc SYSTEM_ADMIN) | Đăng nhập thành công | ☐ |
| 2 | Phê duyệt bước FINANCE | Step APPROVED, request status → `FINANCE_CLEARED` | ☐ |

#### TC-07.4: Bước 4 - Discipline Approval (AUDITOR)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `auditor` | Đăng nhập thành công | ☐ |
| 2 | Phê duyệt bước DISCIPLINE | Step APPROVED, status → `DISCIPLINE_CLEARED` | ☐ |

#### TC-07.5: Bước 5 - Registrar Final Approval (REGISTRAR)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `registrar` | Đăng nhập thành công | ☐ |
| 2 | Phê duyệt bước REGISTRAR | Step APPROVED, status → `FINAL_APPROVED` | ☐ |
| 3 | Kiểm tra tất cả 5 steps đều APPROVED | ✅ All approved | ☐ |
| 4 | Kiểm tra nút "Cấp phát chứng chỉ" xuất hiện | Nút hiển thị (chỉ khi FINAL_APPROVED) | ☐ |

#### TC-07.6: Từ chối (Reject) ở bất kỳ bước nào
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tạo hồ sơ mới, evaluate PASS | Request ở trạng thái sẵn sàng duyệt | ☐ |
| 2 | Ở bước ACADEMIC, click Từ chối (thêm note) | Step → REJECTED | ☐ |
| 3 | Kiểm tra request status | Status → `REJECTED` | ☐ |
| 4 | Kiểm tra LedgerEvent: `APPROVAL_REJECTED` | Event xuất hiện | ☐ |
| 5 | Kiểm tra không thể tiếp tục approval các bước sau | Workflow dừng lại | ☐ |

#### TC-07.7: Phê duyệt sai role
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `studenta`, thử phê duyệt bước ACADEMIC | Bị chặn (403 Forbidden) | ☐ |
| 2 | Đăng nhập `faculty`, thử phê duyệt bước FINANCE | Bị chặn (sai role) | ☐ |

---

### TC-08: Cấp phát Chứng chỉ (Issue Credential)

#### TC-08.1: Issue credential từ hồ sơ FINAL_APPROVED
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở hồ sơ đã FINAL_APPROVED | Nút "Cấp phát chứng chỉ" hiển thị | ☐ |
| 2 | Click cấp phát | Credential mới tạo, status = `ISSUED` | ☐ |
| 3 | Kiểm tra credential có: credential_code, serial_number, verification_code, public_slug | Có đầy đủ | ☐ |
| 4 | Kiểm tra payload_json | Chứa thông tin sinh viên, chương trình, điểm | ☐ |
| 5 | Kiểm tra payload_hash | SHA-256 hash hợp lệ | ☐ |
| 6 | Kiểm tra PDF được tạo | File PDF tồn tại, có thể download | ☐ |
| 7 | Kiểm tra pdf_hash | SHA-256 hash hợp lệ | ☐ |
| 8 | Kiểm tra QR code được tạo | File QR PNG tồn tại | ☐ |
| 9 | Kiểm tra CredentialVersion v1 được tạo | Version 1 có đầy đủ payload | ☐ |
| 10 | Kiểm tra LedgerEvent: `CREDENTIAL_ISSUED` | Event xuất hiện | ☐ |

#### TC-08.2: Xem danh sách chứng chỉ
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào `/chung-chi/` | Danh sách tất cả credentials | ☐ |
| 2 | Kiểm tra cột: code, sinh viên, loại, trạng thái, ngày | Thông tin đúng | ☐ |

#### TC-08.3: Xem chi tiết chứng chỉ
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Click vào credential | Hiển thị đầy đủ detail | ☐ |
| 2 | Kiểm tra: thông tin credential, payload, hashes, PDF preview/download, QR image | Đầy đủ | ☐ |
| 3 | Kiểm tra nút: Ký số, Publish, Thu hồi, Thay thế (tùy trạng thái) | Đúng nút theo status | ☐ |

---

### TC-09: Ký số (Digital Signing)

#### TC-09.1: Ký credential
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `signer` (hoặc `admin`) | Đăng nhập thành công | ☐ |
| 2 | Mở credential có status `ISSUED` | Nút "Ký số" hiển thị | ☐ |
| 3 | Click "Ký số" | Credential được ký, status → `SIGNED` | ☐ |
| 4 | Kiểm tra `signature_value` | Base64-encoded RSA signature tồn tại | ☐ |
| 5 | Kiểm tra `signer_name`, `signer_title` | Thông tin người ký đúng | ☐ |
| 6 | Kiểm tra SignatureRecord | Record mới với: signing_key, signature_algorithm, signed_payload_hash, verified=True | ☐ |
| 7 | Kiểm tra LedgerEvent: `CREDENTIAL_SIGNED` | Event xuất hiện | ☐ |

#### TC-09.2: Signature Verification
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở credential đã SIGNED | Detail page | ☐ |
| 2 | Kiểm tra trạng thái signature verification | Hiển thị "Signature Valid ✓" hoặc tương đương | ☐ |

#### TC-09.3: Ký khi chưa có signing key
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Nếu không có SigningKey active cho organization | Hiển thị lỗi rõ ràng | ☐ |

---

### TC-10: Publish Chứng chỉ

#### TC-10.1: Publish credential
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `registrar` | Đăng nhập thành công | ☐ |
| 2 | Mở credential có status `SIGNED` | Nút "Publish" hiển thị | ☐ |
| 3 | Click "Publish" | Status → `PUBLISHED`, published_at được gán | ☐ |
| 4 | Kiểm tra LedgerEvent: `CREDENTIAL_PUBLISHED` | Event xuất hiện | ☐ |
| 5 | Kiểm tra link "Xem trang xác thực công khai" | Link hiển thị, có thể click | ☐ |

#### TC-10.2: Publish chưa ký
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Thử publish credential chưa SIGNED | Bị chặn, hiển thị lỗi "Cần ký trước khi publish" | ☐ |

---

### TC-11: Thu hồi (Revocation)

#### TC-11.1: Thu hồi credential PUBLISHED
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở credential đã PUBLISHED | Nút "Thu hồi" hiển thị | ☐ |
| 2 | Click "Thu hồi", điền: lý do, số quyết định, ghi chú công khai | Form hiển thị | ☐ |
| 3 | Submit | Status → `REVOKED`, revoked_at được gán | ☐ |
| 4 | Kiểm tra RevocationRecord | Record mới: reason, decision_number, ordered_by, public_note | ☐ |
| 5 | Kiểm tra LedgerEvent: `CREDENTIAL_REVOKED` | Event xuất hiện | ☐ |
| 6 | Xác thực công khai credential này | Hiển thị status "REVOKED" + lý do | ☐ |

#### TC-11.2: Thu hồi credential với attachment
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Thu hồi + upload file đính kèm (quyết định PDF) | Upload thành công | ☐ |
| 2 | Kiểm tra attachment trong RevocationRecord | File tồn tại | ☐ |

---

### TC-12: Thay thế (Supersede)

#### TC-12.1: Supersede credential
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở credential đã PUBLISHED | Nút "Thay thế" hiển thị | ☐ |
| 2 | Click "Thay thế", nhập JSON corrections (VD: sửa tên, sửa điểm) | Form hiển thị | ☐ |
| 3 | Submit | Credential cũ → `SUPERSEDED`, credential mới tạo | ☐ |
| 4 | Kiểm tra credential cũ có `superseded_by` = credential mới | Đúng | ☐ |
| 5 | Kiểm tra credential mới | Có payload merged, hashes mới, PDF mới, QR mới | ☐ |
| 6 | Kiểm tra nếu có signing key → credential mới tự động ký + publish | Auto-sign + auto-publish | ☐ |
| 7 | Kiểm tra LedgerEvent: `CREDENTIAL_SUPERSEDED` | Event xuất hiện | ☐ |

#### TC-12.2: Xác thực credential đã SUPERSEDED
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Xác thực công khai credential cũ | Hiển thị "SUPERSEDED" + link sang bản mới | ☐ |
| 2 | Click link bản mới | Hiển thị credential thay thế | ☐ |

---

### TC-13: Batch Issuance & Merkle Tree

#### TC-13.1: Tạo Batch
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào `/cap-phat/batch/` | Danh sách batch hiển thị | ☐ |
| 2 | Click "Tạo batch", nhập tên, chọn nhiều issuance requests FINAL_APPROVED | Form hiển thị | ☐ |
| 3 | Submit | Batch tạo thành công | ☐ |

#### TC-13.2: Commit Batch (Merkle Root)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở batch detail | Chi tiết batch + danh sách requests | ☐ |
| 2 | Click "Commit" | merkle_root được tính, committed_at + committed_by gán | ☐ |
| 3 | Kiểm tra merkle_root | SHA-256 hash hợp lệ, dựa trên payload_hash của credentials | ☐ |
| 4 | Kiểm tra LedgerEvents liên quan có block_no + batch_no | Backfilled đúng | ☐ |
| 5 | Kiểm tra LedgerEvent: `BATCH_COMMITTED` | Event xuất hiện | ☐ |

#### TC-13.3: Xem batch detail
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở batch đã commit | Hiển thị: merkle_root, committed_at, danh sách credentials | ☐ |
| 2 | Kiểm tra trạng thái committed | is_committed = True | ☐ |

---

### TC-14: Xác thực công khai (Public Verification)

> **Test không cần đăng nhập - truy cập công khai**

#### TC-14.1: Trang tìm kiếm
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở `/xac-thuc/` (không đăng nhập) | Hiển thị form tìm kiếm | ☐ |
| 2 | Giao diện chuyên nghiệp, thân thiện | UI sạch sẽ | ☐ |

#### TC-14.2: Tìm kiếm bằng verification_code
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Nhập verification_code của credential PUBLISHED | Tìm thấy, redirect đến detail | ☐ |
| 2 | Kiểm tra detail hiển thị: loại credential, tên sinh viên (masked), tổ chức cấp, serial, fingerprint | Đúng thông tin | ☐ |
| 3 | Kiểm tra trạng thái signature | "Chữ ký hợp lệ ✓" | ☐ |
| 4 | Kiểm tra trạng thái ledger | "Sổ cái hợp lệ ✓" | ☐ |
| 5 | Kiểm tra trạng thái credential | "VALID" (hoặc "HỢP LỆ") | ☐ |

#### TC-14.3: Tìm kiếm bằng credential_code
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Nhập credential_code | Tìm thấy, hiển thị detail | ☐ |

#### TC-14.4: Tìm kiếm bằng public_slug
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Truy cập `/xac-thuc/tra-cuu/<public_slug>/` | Hiển thị detail trực tiếp | ☐ |

#### TC-14.5: Xác thực credential REVOKED
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tìm credential đã REVOKED | Tìm thấy | ☐ |
| 2 | Kiểm tra hiển thị | Status "REVOKED" + public_note + lý do thu hồi | ☐ |
| 3 | Giao diện cảnh báo rõ ràng (màu đỏ/cảnh báo) | Dễ nhận biết là đã bị thu hồi | ☐ |

#### TC-14.6: Xác thực credential SUPERSEDED
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tìm credential đã SUPERSEDED | Tìm thấy | ☐ |
| 2 | Kiểm tra hiển thị | Status "SUPERSEDED" + link sang bản mới | ☐ |
| 3 | Click link bản mới | Navigate đến credential thay thế | ☐ |

#### TC-14.7: Tìm kiếm không tìm thấy
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Nhập mã không tồn tại: `FAKE-CODE-999` | Thông báo "Không tìm thấy" | ☐ |
| 2 | Nhập giá trị rỗng | Validation error hoặc thông báo nhập mã | ☐ |

#### TC-14.8: Data Privacy
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Kiểm tra MSSV hiển thị ở public page | Bị mask: `12****45` (không hiện đầy đủ) | ☐ |
| 2 | Kiểm tra không hiển thị PII nhạy cảm (CMND, ngày sinh đầy đủ) | Chỉ hiện thông tin được phép | ☐ |

---

### TC-15: QR Code Verification

#### TC-15.1: QR trong PDF
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Download PDF credential đã PUBLISHED | PDF tải về thành công | ☐ |
| 2 | Mở PDF, kiểm tra QR code | QR code hiển thị trong PDF | ☐ |
| 3 | Quét QR bằng điện thoại | Mở URL `/xac-thuc/tra-cuu/<slug>/` trên trình duyệt | ☐ |
| 4 | Trang public hiển thị đúng thông tin credential | Đúng | ☐ |

#### TC-15.2: QR trong trang chi tiết
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Mở chi tiết credential (nội bộ) | QR image hiển thị | ☐ |
| 2 | Quét QR | URL đúng, verify thành công | ☐ |

---

### TC-16: Ledger Explorer & Chain Integrity

#### TC-16.1: Xem sổ cái
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập, vào `/so-cai/` | Danh sách events phân trang (30/trang) | ☐ |
| 2 | Kiểm tra mỗi event hiển thị: sequence, type, entity, actor, timestamp, hash rút gọn | Đầy đủ | ☐ |
| 3 | Events sắp xếp theo sequence_no mới nhất trước | Đúng thứ tự | ☐ |

#### TC-16.2: Xem chi tiết event
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Click vào event | Detail: sequence_no, event_type, entity, actor_user, actor_organization, payload_json, previous_hash, current_hash, is_valid | ☐ |
| 2 | Kiểm tra current_hash khác previous_hash | Đúng (trừ event đầu tiên) | ☐ |
| 3 | Kiểm tra previous_hash = current_hash của event trước | Chain liên kết đúng | ☐ |

#### TC-16.3: Kiểm tra tính toàn vẹn chuỗi (Chain Verification)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào `/so-cai/kiem-tra/` | Trang verification hiển thị | ☐ |
| 2 | Kiểm tra kết quả | `ok: true`, `checked: N`, `issues: []` | ☐ |
| 3 | Hiển thị số events đã kiểm tra | Đúng tổng số | ☐ |

#### TC-16.4: Verify qua CLI
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Chạy `python manage.py verify_ledger` | Output: Chain integrity OK, N events checked | ☐ |

#### TC-16.5: Kiểm tra event types đầy đủ
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Sau khi chạy full flow, kiểm tra sổ cái có đủ events | ISSUANCE_REQUEST_CREATED, ELIGIBILITY_CHECK_PASSED, APPROVAL_GRANTED (x5), CREDENTIAL_ISSUED, CREDENTIAL_SIGNED, CREDENTIAL_PUBLISHED | ☐ |
| 2 | Thu hồi → kiểm tra CREDENTIAL_REVOKED | Có | ☐ |
| 3 | Supersede → kiểm tra CREDENTIAL_SUPERSEDED | Có | ☐ |

---

### TC-17: Audit Logging

#### TC-17.1: Xem audit log
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin`, vào `/kiem-toan/` | Danh sách audit logs | ☐ |
| 2 | Kiểm tra mỗi log có: user, action, object_type, object_id, timestamp | Đầy đủ | ☐ |

#### TC-17.2: Filter audit log
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Filter theo object_type (nếu có tham số GET) | Chỉ hiển thị logs matching filter | ☐ |

#### TC-17.3: Kiểm tra actions được log
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tạo issuance request → kiểm tra audit log | Có log action tương ứng | ☐ |
| 2 | Approve step → kiểm tra audit log | Có log | ☐ |
| 3 | Issue credential → kiểm tra audit log | Có log | ☐ |
| 4 | Sign credential → kiểm tra audit log | Có log | ☐ |
| 5 | Revoke credential → kiểm tra audit log | Có log | ☐ |

---

### TC-18: Reports & Export

#### TC-18.1: Xem báo cáo tổng hợp
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin`, vào `/bao-cao/` | Dashboard báo cáo hiển thị | ☐ |
| 2 | Kiểm tra KPIs: tổng credentials, tổng requests, tổng verifications, revoked, rejected | Số liệu đúng | ☐ |
| 3 | Kiểm tra biểu đồ: by_status, by_type, by_faculty | Charts hiển thị | ☐ |

#### TC-18.2: Export CSV
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Click "Export CSV" (nếu có nút) | File CSV tải về | ☐ |
| 2 | Mở CSV, kiểm tra dữ liệu | Đúng, đầy đủ | ☐ |

#### TC-18.3: Export PDF
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Click "Export PDF" (nếu có nút) | File PDF tải về | ☐ |
| 2 | Mở PDF, kiểm tra dữ liệu | Report styled, đúng | ☐ |

---

### TC-19: REST API Testing

> **Dùng Postman, cURL, hoặc trình duyệt DRF browsable API**

#### TC-19.1: JWT Authentication
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | POST `/api/auth/token/` body: `{"username":"admin","password":"admin12345"}` | Trả về `access` + `refresh` token | ☐ |
| 2 | POST `/api/auth/token/refresh/` body: `{"refresh":"<token>"}` | Trả về access token mới | ☐ |
| 3 | Gọi API không có token | 401 Unauthorized | ☐ |
| 4 | Gọi API với token hết hạn | 401 Unauthorized | ☐ |
| 5 | Gọi API với `Authorization: Bearer <access_token>` | 200 OK, dữ liệu trả về | ☐ |

#### TC-19.2: API CRUD
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | GET `/api/users/` | Danh sách users (paginated) | ☐ |
| 2 | GET `/api/organizations/` | Danh sách organizations | ☐ |
| 3 | GET `/api/students/` | Danh sách students | ☐ |
| 4 | GET `/api/credentials/` | Danh sách credentials | ☐ |
| 5 | GET `/api/issuance-requests/` | Danh sách issuance requests | ☐ |
| 6 | GET `/api/ledger-events/` | Danh sách ledger events | ☐ |
| 7 | GET `/api/policy-rules/` | Danh sách policy rules | ☐ |
| 8 | GET `/api/audit-logs/` | Danh sách audit logs | ☐ |

#### TC-19.3: API Verification (Public, No Auth)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | GET `/api/verification/lookup/?value=<verification_code>` (không có auth header) | Trả về thông tin credential (public-safe) | ☐ |
| 2 | Kiểm tra response không chứa PII nhạy cảm | Masked data | ☐ |

#### TC-19.4: API Report Summary
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | GET `/api/reports/summary/` | JSON response với by_status, by_type, totals | ☐ |

#### TC-19.5: API Pagination
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | GET `/api/ledger-events/?page=1` | Response có: count, next, previous, results | ☐ |
| 2 | GET `/api/ledger-events/?page=2` | Trang tiếp theo | ☐ |

---

### TC-20: Student Portal

#### TC-20.1: Truy cập portal
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `studenta / student12345` | Dashboard sinh viên | ☐ |
| 2 | Vào `/sinh-vien/portal/` | Hiển thị Student Portal | ☐ |
| 3 | Kiểm tra thông tin cá nhân | Đúng: tên, MSSV, khoa, chương trình | ☐ |

#### TC-20.2: Xem credentials của mình
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Portal hiển thị danh sách credentials | Chỉ hiện credentials của student này | ☐ |
| 2 | Kiểm tra có credential PUBLISHED | Có (từ demo data) | ☐ |
| 3 | Click vào credential | Hiển thị detail | ☐ |

#### TC-20.3: Xem issuance requests của mình
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Portal hiển thị danh sách requests | Chỉ hiện requests của student này | ☐ |
| 2 | Kiểm tra trạng thái hiển thị đúng | Đúng | ☐ |

---

### TC-21: Dashboard

#### TC-21.1: Dashboard admin
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin`, vào `/dashboard/` | Dashboard hiển thị | ☐ |
| 2 | Kiểm tra KPIs: credentials issued, pending requests, verifications | Số liệu hợp lý | ☐ |
| 3 | Kiểm tra biểu đồ credential statuses | Chart hiển thị | ☐ |
| 4 | Kiểm tra biểu đồ verification trend (14 ngày) | Chart hiển thị | ☐ |
| 5 | Kiểm tra danh sách recent issuance requests | Hiển thị requests mới nhất | ☐ |
| 6 | Kiểm tra danh sách recent credentials | Hiển thị credentials mới nhất | ☐ |
| 7 | Kiểm tra ledger integrity status | Hiển thị OK/issues | ☐ |

---

### TC-22: Quản lý User & Membership

#### TC-22.1: Tạo user mới
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Đăng nhập `admin`, vào `/tai-khoan/nguoi-dung/` | Danh sách users | ☐ |
| 2 | Click "Tạo người dùng" | Form hiển thị | ☐ |
| 3 | Điền: username, email, password, role, full_name | Tạo thành công | ☐ |
| 4 | Đăng nhập bằng user mới | Thành công | ☐ |

#### TC-22.2: Quản lý membership
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào `/tai-khoan/membership/` | Danh sách memberships | ☐ |
| 2 | Tạo membership: user + organization + role | Tạo thành công | ☐ |
| 3 | Kiểm tra user có thể thao tác với quyền mới | Đúng | ☐ |

#### TC-22.3: Cập nhật hồ sơ cá nhân
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Vào `/tai-khoan/ho-so/` | Hiển thị profile | ☐ |
| 2 | Sửa full_name, phone, job_title | Cập nhật thành công | ☐ |

---

### TC-23: Bảo mật & Access Control

#### TC-23.1: CSRF Protection
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Submit form POST mà không có CSRF token | 403 Forbidden | ☐ |

#### TC-23.2: Session Management
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Kiểm tra cookie session có HttpOnly flag | Có (không truy cập được từ JavaScript) | ☐ |
| 2 | Đăng xuất → cookie session bị xoá | Đúng | ☐ |

#### TC-23.3: URL Traversal
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Truy cập `/chung-chi/<id-credential-khac>/` khi login user thường | Xem được (staff view) hoặc bị chặn (tùy role) | ☐ |
| 2 | Truy cập `/admin/` | Chỉ SYSTEM_ADMIN/staff mới vào được | ☐ |

#### TC-23.4: API Authentication Guard
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | GET `/api/credentials/` không có auth | 401 Unauthorized | ☐ |
| 2 | POST `/api/credentials/` không có auth | 401 Unauthorized | ☐ |
| 3 | GET `/api/verification/lookup/` không có auth | 200 OK (public endpoint) | ☐ |

#### TC-23.5: SQL Injection (Basic check)
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Nhập `' OR 1=1 --` vào search fields | Không crash, không trả data bất thường | ☐ |
| 2 | Nhập `<script>alert(1)</script>` vào input forms | Không execute JS, HTML escaped | ☐ |

#### TC-23.6: File Upload Security
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Upload file revocation attachment là .exe | Bị từ chối hoặc lưu an toàn (không execute) | ☐ |

---

### TC-24: Edge Cases & Error Handling

#### TC-24.1: Duplicate operations
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tạo 2 issuance requests cho cùng 1 student + cùng credential type | Hệ thống xử lý (cho phép hoặc báo lỗi hợp lý) | ☐ |
| 2 | Approve cùng 1 step 2 lần | Lần 2 bị chặn (đã approved) | ☐ |
| 3 | Sign credential đã signed | Bị chặn hoặc overwrite hợp lý | ☐ |
| 4 | Publish credential đã published | Bị chặn | ☐ |
| 5 | Revoke credential đã revoked | Bị chặn | ☐ |

#### TC-24.2: Invalid state transitions
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Thử issue credential khi request chưa FINAL_APPROVED | Bị chặn | ☐ |
| 2 | Thử sign credential ở trạng thái DRAFT | Bị chặn | ☐ |
| 3 | Thử publish credential chưa signed | Bị chặn | ☐ |

#### TC-24.3: Missing data
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Tạo issuance request không chọn student | Form validation error | ☐ |
| 2 | Tạo issuance request không chọn credential type | Form validation error | ☐ |

#### TC-24.4: Concurrent access
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | 2 người duyệt cùng 1 step cùng lúc | Chỉ 1 người thành công (hoặc ghi đè hợp lý) | ☐ |

---

### TC-25: Email Notifications

> **Kiểm tra email console output (dev mode) hoặc email thực (nếu config SendGrid)**

#### TC-25.1: Notification khi credential issued
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Issue credential → kiểm tra console | Email notification gửi đến student | ☐ |
| 2 | Kiểm tra nội dung email | Template đúng, thông tin credential đúng | ☐ |

#### TC-25.2: Notification khi published
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Publish credential → kiểm tra console | Email gửi, có link public verification | ☐ |

#### TC-25.3: Notification khi revoked
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Revoke credential → kiểm tra console | Email gửi, có lý do thu hồi | ☐ |

#### TC-25.4: Notification khi approval step
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Approve/reject step → kiểm tra console | Email notification gửi | ☐ |

---

### TC-26: Performance & Rate Limiting

#### TC-26.1: Rate limiting public verification
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Gọi `/api/verification/lookup/` 30+ lần liên tiếp trong 1 phút | Sau ngưỡng → 429 Too Many Requests | ☐ |

#### TC-26.2: Rate limiting anonymous API
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Gọi API endpoint anonymous 30+ lần/phút | Sau ngưỡng → 429 | ☐ |

#### TC-26.3: Pagination
| # | Bước | Kết quả mong đợi | Pass/Fail |
|---|------|------------------|-----------|
| 1 | Ledger events list với 100+ events | Phân trang 30/trang, load nhanh | ☐ |
| 2 | API pagination | Trả về count, next, previous links | ☐ |

---

## D. Checklist tổng hợp

### Luồng chính (Happy Path) - End-to-End
| # | Checkpoint | Pass/Fail |
|---|-----------|-----------|
| 1 | Đăng nhập thành công | ☐ |
| 2 | Tạo issuance request | ☐ |
| 3 | Evaluate policy rules → PASS | ☐ |
| 4 | Approve ACADEMIC → PASS | ☐ |
| 5 | Approve EXAMINATION → PASS | ☐ |
| 6 | Approve FINANCE → PASS | ☐ |
| 7 | Approve DISCIPLINE → PASS | ☐ |
| 8 | Approve REGISTRAR → FINAL_APPROVED | ☐ |
| 9 | Issue credential → ISSUED + PDF + QR | ☐ |
| 10 | Sign credential → SIGNED | ☐ |
| 11 | Publish credential → PUBLISHED | ☐ |
| 12 | Public verification → VALID | ☐ |
| 13 | QR scan → VALID | ☐ |
| 14 | Revoke credential → REVOKED | ☐ |
| 15 | Supersede credential → SUPERSEDED + bản mới | ☐ |
| 16 | Ledger chain integrity → OK | ☐ |
| 17 | Audit log ghi đầy đủ | ☐ |
| 18 | Report hiển thị đúng | ☐ |

### Luồng lỗi (Error Path)
| # | Checkpoint | Pass/Fail |
|---|-----------|-----------|
| 1 | Evaluate policy → FAIL (GPA thấp) | ☐ |
| 2 | Evaluate policy → FAIL (finance hold) | ☐ |
| 3 | Evaluate policy → FAIL (thiếu credits) | ☐ |
| 4 | Reject ở bước approval | ☐ |
| 5 | Truy cập không đủ quyền → 403 | ☐ |
| 6 | API không auth → 401 | ☐ |
| 7 | Tìm credential không tồn tại | ☐ |
| 8 | Invalid state transition bị chặn | ☐ |

### Blockchain Properties
| # | Checkpoint | Pass/Fail |
|---|-----------|-----------|
| 1 | Mỗi action tạo LedgerEvent | ☐ |
| 2 | Hash chain liên tục (previous_hash → current_hash) | ☐ |
| 3 | SHA-256 payload integrity | ☐ |
| 4 | RSA-2048 digital signature | ☐ |
| 5 | Signature verification hoạt động | ☐ |
| 6 | Merkle root tính đúng (batch) | ☐ |
| 7 | Chain verification phát hiện tamper | ☐ |
| 8 | Multi-party approval (consensus) hoạt động | ☐ |
| 9 | Immutability: events không bị sửa/xoá | ☐ |
| 10 | Public verification không cần đăng nhập | ☐ |

### UX/UI
| # | Checkpoint | Pass/Fail |
|---|-----------|-----------|
| 1 | Sidebar navigation đầy đủ, đúng role | ☐ |
| 2 | Responsive trên mobile | ☐ |
| 3 | Messages/flash notifications hiển thị rõ | ☐ |
| 4 | Form validation errors hiển thị inline | ☐ |
| 5 | Loading state cho operations lâu | ☐ |
| 6 | Breadcrumb/navigation rõ ràng | ☐ |
| 7 | Trang public verification chuyên nghiệp | ☐ |
| 8 | PDF credential có QR, thông tin đầy đủ, design đẹp | ☐ |

---

## Ghi chú cho tester

1. **Thứ tự test**: Nên test theo đúng thứ tự TC-01 → TC-26 vì các test case sau phụ thuộc kết quả của test trước

2. **Multi-browser**: Cần ít nhất 2 session (browser + incognito) để test multi-role approval workflow

3. **Console output**: Kiểm tra terminal chạy `runserver` để xem email notifications (chế độ dev dùng console backend)

4. **Database reset**: Nếu dữ liệu bị hỏng, chạy `python manage.py seed_demo_data --reset` để reset

5. **Signing key**: Đảm bảo đã chạy `python manage.py generate_sample_keys` trước khi test signing

6. **Ghi lại bugs**: Mỗi khi một test case FAIL, ghi lại:
   - Bước bị fail
   - Kết quả thực tế (screenshot nếu có)
   - Error message (nếu có)
   - Console log (nếu có)
