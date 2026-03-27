# KỊCH BẢN DEMO — Hệ thống Quản lý Văn bằng số HCMUTE

> **Môn:** Blockchain Ứng dụng — Đồ án cuối kỳ  
> **Hệ thống:** Permissioned Blockchain Credential Ledger  
> **URL:** http://127.0.0.1:8000  
> **Thời gian demo đề xuất:** 20–25 phút

---

## PHẦN 0 — Chuẩn bị trước khi demo

Mở sẵn **3 cửa sổ trình duyệt** (hoặc 3 tab incognito):

| Cửa sổ | Mục đích |
|--------|----------|
| A — Tab chính | Đăng nhập thay đổi theo role |
| B — Tab sinh viên | Đăng nhập `ntnhat` xem cổng cá nhân |
| C — Tab công khai | Mở `/xac-thuc/`, không cần đăng nhập |

**Tài khoản demo:**

| Username | Password | Role | Thuộc tổ chức |
|----------|----------|------|---------------|
| `admin` | `admin12345` | System Admin | HCMUTE |
| `faculty` | `faculty12345` | Faculty Admin | Khoa CNTT |
| `registrar` | `registrar12345` | Registrar | Phòng Văn bằng |
| `signer` | `signer12345` | Signer | Phòng Văn bằng |
| `auditor` | `auditor12345` | Auditor | Phòng Kiểm định |
| `ntnhat` | `student12345` | Student | Nguyễn Thanh Nhật |
| `nmkhoi` | `student12345` | Student | Nguyễn Minh Khôi |
| `tdhoa` | `student12345` | Student | Trần Doãn Hòa |

---

## PHẦN 1 — Tổng quan hệ thống (2 phút)

### Bước 1.1 — Đăng nhập Admin, xem Dashboard

1. Mở http://127.0.0.1:8000 → tự redirect về trang đăng nhập
2. Đăng nhập `admin / admin12345`
3. Dashboard hiển thị:
   - Tổng số sinh viên, chứng chỉ, hồ sơ đang chờ
   - Biểu đồ trạng thái chứng chỉ (doughnut chart)
   - Trạng thái tính toàn vẹn Ledger (**Ledger Integrity: OK**)

> 💬 **Nói:** "Đây là trang tổng quan của người quản trị. Mọi hoạt động quan trọng đều được ghi vào sổ cái (ledger) — tương tự blockchain — và hệ thống tự động kiểm tra tính toàn vẹn của chuỗi hash sau mỗi giao dịch."

### Bước 1.2 — Xem danh sách sinh viên

1. Sidebar → **Sinh viên**
2. Danh sách 5 sinh viên, cột GPA màu xanh/vàng/đỏ, icon ✓/✗ cho điều kiện tốt nghiệp
3. Click vào **Nguyễn Thanh Nhật** → xem chi tiết

> 💬 "Mỗi sinh viên có hồ sơ học thuật đầy đủ: GPA, tín chỉ, chương trình đào tạo — đây là dữ liệu đầu vào cho rule engine đánh giá điều kiện tốt nghiệp, giống smart contract trong blockchain thực."

---

## PHẦN 2 — Rule Engine (Smart Contract tương tự) (3 phút)

### Bước 2.1 — Tạo hồ sơ cấp phát mới

1. **Đổi đăng nhập sang `faculty / faculty12345`**
2. Sidebar → **Hồ sơ cấp phát** → nút **Tạo hồ sơ mới**
3. Điền form:
   - **Student:** chọn `Nguyễn Thanh Nhật` (SV có đủ điều kiện)
   - **Credential Type:** `Bằng tốt nghiệp`
   - **Template:** `Mẫu bằng tốt nghiệp`
   - **Notes:** `Demo trực tiếp — HK2/2025`
4. Nhấn **Tạo** → redirect sang trang chi tiết hồ sơ

> 💬 "Hồ sơ vừa được tạo trong trạng thái `SUBMITTED`. Hệ thống tự động sinh 5 bước phê duyệt tương ứng 5 vai trò: Academic → Examination → Finance → Discipline → Registrar. Đây chính là cơ chế **consensus nhiều bên** trong môi trường đại học."

### Bước 2.2 — Chạy Policy Rules Evaluation

1. Trong trang chi tiết hồ sơ, nhấn nút **Chạy đánh giá điều kiện**
2. Kết quả hiển thị từng rule:
   - `RULE-CREDITS` — ✅ PASS (đã đủ tín chỉ)
   - `RULE-GPA` — ✅ PASS (GPA ≥ tối thiểu)
   - `RULE-FINANCE` — ✅ PASS (không có hold tài chính)
   - `RULE-DISCIPLINE` — ✅ PASS (không có hold kỷ luật)

> 💬 "Rule engine hoạt động như smart contract: mỗi rule được định nghĩa bằng JSON logic condition, hệ thống tự động so sánh dữ liệu sinh viên với ngưỡng của chương trình đào tạo. Không cần can thiệp thủ công."

### Bước 2.3 — Demo sinh viên KHÔNG đủ điều kiện (tùy chọn, ~1 phút)

1. Sidebar → **Hồ sơ cấp phát** → tìm hồ sơ của **Lê Quang Huy** (đã seeded)
2. Xem kết quả evaluation: `RULE-FINANCE` — ❌ FAIL (`finance_hold = True`)
3. Hồ sơ `UNDER_REVIEW` — không thể tiến hành tiếp

> 💬 "Đây là tính chất tamper-proof của rule engine: sinh viên chưa giải quyết nợ tài chính thì hệ thống tự động chặn, không ai có thể bypass bằng tay."

---

## PHẦN 3 — Approval Workflow (Đồng thuận nhiều bước) (4 phút)

> Tiếp tục với hồ sơ của Nguyễn Thanh Nhật vừa tạo ở Phần 2.

### Bước 3.1 — Phê duyệt bước ACADEMIC (role: Faculty Admin)

1. Vẫn đăng nhập `faculty`
2. Trong trang chi tiết hồ sơ → ô **ACADEMIC** → điền ghi chú → nhấn **Phê duyệt**
3. Badge chuyển từ `PENDING` → `APPROVED`

### Bước 3.2 — Phê duyệt bước EXAMINATION, FINANCE, DISCIPLINE (role: Admin)

1. **Đổi sang `admin / admin12345`**
2. Mở lại hồ sơ → phê duyệt lần lượt 3 bước còn lại (Examination, Finance, Discipline)

### Bước 3.3 — Phê duyệt cuối: REGISTRAR

1. **Đổi sang `registrar / registrar12345`**
2. Mở hồ sơ → bước **REGISTRAR** → phê duyệt
3. Trạng thái hồ sơ chuyển sang **`ALL_APPROVED`**

> 💬 "5 bước phê duyệt hoàn tất. Giống như trong mạng blockchain có permissioned validators — mỗi node (phòng ban) phải đồng thuận trước khi giao dịch được xác nhận. Không bước nào có thể bị bỏ qua."

---

## PHẦN 4 — Issue, Ký số & Publish Chứng chỉ (4 phút)

### Bước 4.1 — Issue Credential (sinh payload + PDF)

1. Vẫn đăng nhập `registrar`
2. Trong trang chi tiết hồ sơ → nhấn **Cấp phát chứng chỉ (Issue)**
3. Hệ thống:
   - Sinh `credential_code` (VD: `CRD-XXXXXXXX`)
   - Tạo payload JSON chứa thông tin sinh viên, chương trình, ngày cấp
   - Tính **SHA-256 hash** của payload
   - Render file **PDF** chứng chỉ
   - Ghi **LedgerEvent** `CREDENTIAL_ISSUED` vào sổ cái
4. Redirect sang trang chi tiết chứng chỉ
5. Nhấn **Tải PDF** để xem file chứng chỉ

> 💬 "Chứng chỉ được hash SHA-256 ngay khi tạo. Bất kỳ thay đổi nào sau này — dù chỉ 1 ký tự — đều bị phát hiện qua hash. Đây là nền tảng tamper-evidence của hệ thống."

### Bước 4.2 — Ký số RSA (Digital Signature)

1. **Đổi sang `signer / signer12345`**
2. Mở trang chứng chỉ vừa issue
3. Trong ô **Ký số** → chọn signing key `Demo Registrar Key` → nhấn **Ký**
4. Hệ thống ký RSA payload hash bằng private key
5. Ghi **LedgerEvent** `CREDENTIAL_SIGNED`

> 💬 "Chữ ký RSA gắn với private key của Phòng Công tác Sinh viên. Khi xác thực, hệ thống dùng public key để verify chữ ký — đảm bảo chứng chỉ do đúng tổ chức phát hành, không bị làm giả."

### Bước 4.3 — Publish (công bố công khai)

1. Vẫn là `signer` hoặc đổi lại `registrar`
2. Nhấn **Publish** → trạng thái chuyển `PUBLISHED`
3. Hệ thống sinh:
   - `verification_code` (dạng `VER-XXXXXXXX`)
   - `public_slug` (URL công khai duy nhất)
   - Mã **QR code** nhúng trong PDF và trang chi tiết
   - Ghi **LedgerEvent** `CREDENTIAL_PUBLISHED`

> 💬 "Sau khi publish, chứng chỉ có link xác thực công khai và QR code. Bất kỳ ai — nhà tuyển dụng, trường đối tác — có thể quét QR hoặc nhập mã để xác thực mà không cần tài khoản."

---

## PHẦN 5 — Cổng Xác thực Công khai (3 phút)

### Bước 5.1 — Xác thực chứng chỉ hợp lệ (Tab C — không đăng nhập)

1. Mở **Tab C**: http://127.0.0.1:8000/xac-thuc/
2. Copy `verification_code` từ trang chi tiết chứng chỉ vừa publish (VD: `VER-XXXXXXXX`)
3. Dán vào ô tìm kiếm → nhấn **Xác thực**
4. Kết quả:
   - ✅ **HỢP LỆ**
   - Tên sinh viên: Nguyễn Thanh Nhật
   - Chương trình: Công nghệ thông tin
   - Chữ ký số: **Hợp lệ**
   - Ledger: **Hợp lệ**

> 💬 "Đây là luồng mà nhà tuyển dụng sẽ sử dụng. Không cần tài khoản, không cần liên hệ trường. Hệ thống tự động verify chữ ký RSA và kiểm tra hash trong ledger."

### Bước 5.2 — Xác thực chứng chỉ đã bị thu hồi (REVOKED)

1. Sidebar (Tab A) → **Chứng chỉ** → tìm chứng chỉ của **Nguyễn Minh Khôi** (status: `REVOKED`)
2. Copy verification code
3. Quay sang **Tab C** → dán vào tìm kiếm
4. Kết quả:
   - ❌ **ĐÃ BỊ THU HỒI**
   - Lý do: `Fraud detected in supporting document`
   - Quyết định thu hồi: `QD-TH-2026-001`

> 💬 "Ngay cả khi chứng chỉ đã được cấp và ký số, trường vẫn có thể thu hồi nếu phát hiện gian lận. Hành động thu hồi được ghi vĩnh viễn vào ledger — không thể xóa lịch sử."

### Bước 5.3 — Xác thực chứng chỉ SUPERSEDED (bị thay thế)

1. Tìm chứng chỉ của **Trần Doãn Hòa** (status: `SUPERSEDED`)
2. Copy verification code → dán vào Tab C
3. Kết quả: **ĐÃ BỊ THAY THẾ** — hệ thống hiển thị link sang bản mới
4. Click vào bản mới → trạng thái `PUBLISHED`, thông tin đã được cập nhật

> 💬 "Supersede cho phép đính chính thông tin (VD: sai tên, sai chương trình) mà vẫn bảo toàn lịch sử. Bản cũ không bị xóa — ledger ghi đầy đủ chuỗi phiên bản."

---

## PHẦN 6 — Cổng Sinh viên (2 phút)

### Bước 6.1 — Sinh viên xem chứng chỉ của mình

1. **Tab B** → đăng nhập `ntnhat / student12345`
2. Redirect về cổng sinh viên tại `/sinh-vien/cong-tua/`
3. Hiển thị:
   - Hồ sơ cá nhân, GPA, tín chỉ
   - Danh sách chứng chỉ đã được cấp
   - Nút **Xem công khai** và **Tải PDF**

> 💬 "Sinh viên có thể tự chia sẻ link xác thực cho nhà tuyển dụng mà không cần liên hệ phòng đăng ký."

---

## PHẦN 7 — Ledger & Tính toàn vẹn Blockchain (3 phút)

### Bước 7.1 — Xem Ledger Explorer

1. Tab A (đăng nhập `admin`) → Sidebar → **Ledger**
2. Danh sách tất cả sự kiện, sắp xếp theo `sequence_no`:
   - `ISSUANCE_REQUEST_CREATED`
   - `POLICY_EVALUATED`
   - `APPROVAL_STEP_APPROVED` × 5
   - `CREDENTIAL_ISSUED`
   - `CREDENTIAL_SIGNED`
   - `CREDENTIAL_PUBLISHED`
3. Click vào một event → xem `previous_hash`, `current_hash`, `payload_json`

> 💬 "Mỗi event lưu hash của event trước — tạo thành chuỗi hash chain không thể giả mạo, giống cấu trúc block trong blockchain. Nếu ai sửa dữ liệu trong database, chuỗi hash sẽ bị gãy ngay lập tức."

### Bước 7.2 — Verify toàn bộ chain (Ledger Integrity Check)

1. Sidebar → **Ledger** → nút **Kiểm tra tính toàn vẹn**
2. Hoặc chạy lệnh terminal:
   ```bash
   docker exec project-web-1 python manage.py verify_ledger
   ```
3. Kết quả:
   - ✅ `Chain valid: True`
   - Tổng số event đã verify
   - Không có event nào bị tamper

> 💬 "Đây là tính năng tương đương `Full Node Verification` trong blockchain thực. Bất kỳ ai có quyền admin đều có thể chạy kiểm tra độc lập để xác nhận toàn bộ lịch sử hệ thống chưa bị can thiệp."

---

## PHẦN 8 — Kiểm toán & Báo cáo (2 phút)

### Bước 8.1 — Audit Log

1. Sidebar → **Kiểm toán**
2. Mọi hành động trong hệ thống đều được log: ai làm gì, lúc nào, với đối tượng nào
3. Filter theo user, loại hành động, thời gian

### Bước 8.2 — Báo cáo thống kê

1. Sidebar → **Báo cáo**
2. Dashboard thống kê: số chứng chỉ theo trạng thái, theo chương trình, theo thời gian

---

## PHẦN 9 — REST API (tùy chọn, 1 phút)

Mở http://127.0.0.1:8000/api/ — minh chứng hệ thống có thể tích hợp với ứng dụng bên ngoài:

```bash
# Xác thực công khai qua API (không cần đăng nhập)
curl "http://127.0.0.1:8000/api/verification/lookup/?value=VER-XXXXXXXX"
```

Response:
```json
{
  "credential_code": "CRD-XXXXXXXX",
  "status": "VALID",
  "owner_name": "Nguyễn Thanh Nhật",
  "issuer_name": "Phòng Công tác Sinh viên & Quản lý Văn bằng",
  "signature_valid": true,
  "ledger_valid": true
}
```

---

## ĐIỂM NHẤN KHI THUYẾT TRÌNH

| Khái niệm Blockchain | Hiện thực trong hệ thống |
|---------------------|--------------------------|
| Block | `LedgerEvent` với `sequence_no`, `previous_hash`, `current_hash` |
| Hash chain | Mỗi event hash tích lũy từ event trước → phát hiện giả mạo |
| Smart Contract | `PolicyRule` JSON — rule engine tự động đánh giá điều kiện |
| Permissioned Nodes | Approval workflow 5 bước — mỗi role là một validator |
| Digital Signature | RSA sign payload hash bằng private key của tổ chức |
| Immutability | Revoke/Supersede không xóa bản cũ — lịch sử luôn được giữ |
| Public Verification | Cổng `/xac-thuc/` + QR code — verify không cần tài khoản |
| Consensus | Tất cả 5 approval bước phải `APPROVED` mới được issue |

---

## THỨ TỰ DEMO TỐI ƯU (20 phút)

```
[P1] Dashboard + Sinh viên          2' — Giới thiệu hệ thống
[P2] Tạo hồ sơ + Rule Evaluation    3' — Smart contract / Rule engine
[P3] Approval Workflow               4' — Consensus nhiều bên
[P4] Issue + Sign + Publish          4' — Hash, RSA, QR
[P5] Public Portal xác thực          3' — Tamper-evidence thực tế
[P6] Cổng sinh viên                  1' — UX người dùng cuối
[P7] Ledger + Verify chain           2' — Blockchain core
[P8] Audit + Report                  1' — Quản trị hệ thống
```
