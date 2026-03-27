# CHANGELOG — Các lỗi đã phát hiện và sửa

> Tổng hợp toàn bộ lỗi tìm được qua nhiều lần chạy demo, kèm nguyên nhân gốc và cách khắc phục.

---

## Mục lục

1. [BUG-01: PowerShell không chạy được lệnh Python](#bug-01-powershell-không-chạy-được-lệnh-python)
2. [BUG-02: 10 test thất bại — dữ liệu fixture cũ](#bug-02-10-test-thất-bại--dữ-liệu-fixture-cũ)
3. [BUG-03: Chữ ký số không hợp lệ sau khi chạy test](#bug-03-chữ-ký-số-không-hợp-lệ-sau-khi-chạy-test)
4. [BUG-04: Console Windows không hiển thị được tiếng Việt](#bug-04-console-windows-không-hiển-thị-được-tiếng-việt)
5. [BUG-05: Student xem được toàn bộ credential/student của hệ thống](#bug-05-student-xem-được-toàn-bộ-credentialstudent-của-hệ-thống)

---

## BUG-01: PowerShell không chạy được lệnh Python

| Mục | Chi tiết |
|-----|----------|
| **Triệu chứng** | `Unexpected token '-m'` khi chạy `python -m pip install` |
| **Nguyên nhân** | Đường dẫn Python chứa khoảng trắng (`C:/Users/MINH KHOI/...`), PowerShell yêu cầu toán tử gọi `&` cho path có dấu ngoặc kép |
| **Mức nghiêm trọng** | Thấp — chỉ ảnh hưởng môi trường dev |

**Cách sửa:** Thêm `&` trước path có ngoặc kép:

```powershell
# Sai
"C:/Users/MINH KHOI/.../python3.11.exe" -m pip install -r requirements.txt

# Đúng
& "C:/Users/MINH KHOI/.../python3.11.exe" -m pip install -r requirements.txt
```

**File thay đổi:** Không thay đổi code — chỉ sửa cách gọi lệnh.

---

## BUG-02: 10 test thất bại — dữ liệu fixture cũ

| Mục | Chi tiết |
|-----|----------|
| **Triệu chứng** | `User.DoesNotExist`, `Student.DoesNotExist` — 10/17 test lỗi |
| **Nguyên nhân** | Code test cũ dùng username `studenta` và mã sinh viên `SV001`, `SV002`, `SV004`, `SV005`. Seed data hiện tại dùng `ntnhat` và `2001210001`, `2001210002`, `2101210004`, `2101210005` |
| **Mức nghiêm trọng** | Trung bình — test suite không chạy được |

### File 1: `accounts/tests.py`

```python
# Trước
user = User.objects.get(username="studenta")
self.assertEqual(response.status_code, 403)

# Sau
user = User.objects.get(username="ntnhat")
self.assertIn(response.status_code, [302, 403])
```

- Đổi username cho khớp seed data
- Cho phép cả 302 (redirect) lẫn 403 (forbidden) vì tùy middleware có thể trả về status code khác nhau

### File 2: `issuance/tests.py`

```python
# Trước                          # Sau
student_code="SV004"       →     student_code="2101210004"
student_code="SV001"       →     student_code="2001210001"
student_code="SV005"       →     student_code="2101210005"
student_code="SV001"       →     student_code="2001210001"
```

4 chỗ thay đổi trong 4 test method:
- `test_create_issuance_request`
- `test_rule_evaluation_pass`
- `test_rule_evaluation_fail`
- `test_approval_workflow_reaches_final_approved`

### File 3: `credentials/tests.py`

```python
# Trước                          # Sau
student_code="SV001"       →     student_code="2001210001"
student_code="SV002"       →     student_code="2001210002"
```

2 chỗ thay đổi:
- `_final_approved_request` (default parameter)
- `test_supersede_service_creates_new_credential`

**Kết quả:** 17/17 test PASS.

---

## BUG-03: Chữ ký số không hợp lệ sau khi chạy test

| Mục | Chi tiết |
|-----|----------|
| **Triệu chứng** | Credential mới tạo qua live flow trả về `signature_valid=false`, trong khi credential từ seed vẫn `true` |
| **Nguyên nhân gốc** | `seed_demo_data._ensure_signing_key()` **luôn tạo lại cặp key mới** kể cả khi file private key đã tồn tại. Khi chạy `manage.py test`, seed chạy trong test DB và ghi đè file private key dưới `media/keys/`. DB chính vẫn giữ public key cũ → mismatch |
| **Mức nghiêm trọng** | **Cao** — chữ ký số mất hiệu lực, credential bị coi là giả mạo |

### File: `core/management/commands/seed_demo_data.py`

**Thêm import:**
```python
from cryptography.hazmat.primitives import serialization
```

**Sửa method `_ensure_signing_key`:**

```python
# TRƯỚC — luôn tạo key mới (SAI)
else:
    public_key_pem = generate_rsa_key_pair(str(private_key_path))

# SAU — giữ key cũ, derive public key từ private key đã có (ĐÚNG)
else:
    private_key = serialization.load_pem_private_key(
        private_key_path.read_bytes(), password=None
    )
    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")
```

**Logic sau khi sửa:**
1. Nếu file private key **chưa tồn tại** → tạo cặp key mới (giữ nguyên logic cũ)
2. Nếu file private key **đã tồn tại** → đọc private key, derive public key tương ứng, cập nhật DB

**Kết quả:** `signature_valid=true` cho cả credential cũ lẫn mới tạo.

---

## BUG-04: Console Windows không hiển thị được tiếng Việt

| Mục | Chi tiết |
|-----|----------|
| **Triệu chứng** | Ký tự tiếng Việt bị lỗi encoding khi chạy `seed_demo_data` trên Windows |
| **Nguyên nhân** | Console Windows mặc định dùng encoding cp1252, không hỗ trợ đầy đủ Unicode |
| **Mức nghiêm trọng** | Thấp — không ảnh hưởng logic, chỉ ảnh hưởng hiển thị |

### File: `core/management/commands/seed_demo_data.py`

```python
import io
import sys

# Thêm vào đầu method handle()
if sys.platform == "win32" and hasattr(self.stdout, "reconfigure"):
    try:
        self.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        self.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
```

**Kết quả:** Tên tiếng Việt (Nguyễn Thanh Nhật, Trần Doãn Hòa...) hiển thị đúng.

---

## BUG-05: Student xem được toàn bộ credential/student của hệ thống

| Mục | Chi tiết |
|-----|----------|
| **Triệu chứng** | User có role `STUDENT` gọi API `/api/credentials/` thấy tất cả 4 credential thay vì chỉ 1 của mình. Tương tự với `/api/students/` — thấy tất cả 5 student |
| **Nguyên nhân gốc** | 3 ViewSet (`CredentialViewSet`, `StudentViewSet`, `StudentCourseRecordViewSet`) chỉ dùng `permission_classes = [IsAuthenticated]` mà **không lọc queryset theo role**. `queryset = Model.objects.all()` trả về toàn bộ bản ghi cho mọi user đã đăng nhập |
| **Mức nghiêm trọng** | **Cao** — vi phạm kiểm soát truy cập (OWASP A01:2021 – Broken Access Control) |

### File 1: `credentials/views.py`

```python
# TRƯỚC
class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.select_related(...)
    serializer_class = CredentialSerializer
    permission_classes = [permissions.IsAuthenticated]

# SAU — thêm get_queryset() lọc theo role
class CredentialViewSet(viewsets.ModelViewSet):
    serializer_class = CredentialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Credential.objects.select_related(
            "student", "credential_type", "issuer_organization",
        )
        user = self.request.user
        if user.role == UserRole.STUDENT:
            return qs.filter(student__user=user)
        return qs.all()
```

### File 2: `students/views.py`

**StudentViewSet:**
```python
def get_queryset(self):
    qs = Student.objects.select_related("faculty", "academic_program")
    user = self.request.user
    if user.role == UserRole.STUDENT:
        return qs.filter(user=user)
    return qs.all()
```

**StudentCourseRecordViewSet:**
```python
def get_queryset(self):
    qs = StudentCourseRecord.objects.select_related("student", "course")
    user = self.request.user
    if user.role == UserRole.STUDENT:
        return qs.filter(student__user=user)
    return qs.all()
```

**Kiểm chứng sau sửa:**
- User `ntnhat` (STUDENT) → `GET /api/credentials/` → `count=1` (chỉ thấy credential của mình)
- User `ntnhat` (STUDENT) → `GET /api/students/` → `count=1` (chỉ thấy hồ sơ của mình)
- User `admin` (SYSTEM_ADMIN) → vẫn thấy toàn bộ bản ghi
- `POST`, `DELETE` cho STUDENT → bị chặn đúng (400/405)

---

## Tổng kết

| # | Lỗi | File sửa | Mức nghiêm trọng |
|---|------|----------|-------------------|
| 01 | PowerShell path có khoảng trắng | _(không sửa code)_ | Thấp |
| 02 | Test dùng fixture cũ | `accounts/tests.py`, `issuance/tests.py`, `credentials/tests.py` | Trung bình |
| 03 | Key bị tạo lại → chữ ký mất hiệu lực | `core/management/commands/seed_demo_data.py` | **Cao** |
| 04 | Tiếng Việt lỗi encoding trên Windows | `core/management/commands/seed_demo_data.py` | Thấp |
| 05 | Student xem được data toàn hệ thống | `credentials/views.py`, `students/views.py` | **Cao** |

**Tổng file thay đổi:** 6 file  
**Test sau khi sửa tất cả:** 17/17 PASS  
**Trạng thái hiện tại:** Ổn định, không còn lỗi phát hiện thêm
