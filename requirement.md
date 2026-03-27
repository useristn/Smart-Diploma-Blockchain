Bạn là Principal Software Architect, Senior Python Full-Stack Engineer, Blockchain Systems Designer, DevOps Engineer, Security Engineer, QA Lead và Technical Writer trong cùng một vai trò.

Nhiệm vụ của bạn là thiết kế và sinh ra TOÀN BỘ một hệ thống web hoàn chỉnh, chạy được thực tế, dùng PYTHON làm ngôn ngữ chính, phục vụ đồ án:

“Xây dựng hệ thống cấp phát và xác thực chứng chỉ số / bằng cấp số cho sinh viên ứng dụng công nghệ blockchain”

Mục tiêu là tạo ra một web app full-stack hoàn chỉnh, chạy được thật, có database, có đăng nhập phân quyền, có giao diện web, có API, có dữ liệu mẫu, có cấp phát chứng chỉ, có xác thực công khai bằng QR, có cơ chế ledger chống sửa đổi kiểu blockchain nội bộ / permissioned blockchain, có chữ ký số ở mức ứng dụng, có workflow kiểm duyệt, có thu hồi chứng chỉ, có nhật ký kiểm toán, có tài liệu README, có test, có Docker, có dữ liệu demo, có mô tả kiến trúc gắn với các kiến thức từ CHƯƠNG 1 đến CHƯƠNG 6 của môn blockchain.

Hệ thống KHÔNG được là demo sơ sài hoặc pseudo-code. Không dùng TODO, không bỏ trống business logic, không chỉ dựng giao diện mẫu. Hệ thống phải đủ để chạy local bằng Docker hoặc chạy trực tiếp trên máy. Hệ thống phải thể hiện được tinh thần blockchain trong môn học, nhưng phù hợp phạm vi đồ án sinh viên và môi trường đại học.

==================================================
I. TRIẾT LÝ THIẾT KẾ GẮN VỚI CHƯƠNG 1 -> CHƯƠNG 6
==================================================

Bạn phải thiết kế hệ thống sao cho phản ánh đầy đủ tinh thần học phần blockchain của tôi như sau:

1. CHƯƠNG 1 – Money, Ledger, Good Ledger, Payment System
- Hệ thống phải coi credential issuance/verification như một bài toán ledger:
  - ghi nhận các thay đổi trạng thái chứng chỉ
  - ai cấp
  - cấp cho ai
  - vào thời điểm nào
  - theo quyết định nào
  - có bị thu hồi hay không
- Ledger phải có đầy đủ các tính chất:
  - immutable
  - timestamped
  - ownership
  - accuracy
  - description of transaction
  - comprehensive
- Hệ thống phải mô hình hóa “credential transaction” tương tự tư duy transaction trong blockchain:
  - issue credential
  - sign credential
  - publish credential
  - verify credential
  - revoke / suspend / re-issue credential
- Giải thích bằng design và code rằng đây là “distributed trust for credential record”, không chỉ là CRUD database thông thường.

2. CHƯƠNG 2 – Cryptography, Hash, Timestamped Append-only Logs, Merkle, Digital Signature
- Hệ thống phải dùng:
  - cryptographic hash functions
  - timestamped append-only ledger
  - digital signatures
  - document fingerprint
  - verification proof
- Mỗi chứng chỉ phải có:
  - nội dung dữ liệu chuẩn hóa
  - hash của payload
  - hash của file PDF
  - previous_hash / current_hash trong ledger
  - signature của issuer hoặc signing authority
- Có khả năng verify lại:
  - dữ liệu chứng chỉ
  - file chứng chỉ
  - QR verification
  - integrity của ledger chain
- Nếu hợp lý, có thể thêm Merkle-root hoặc batch issuance proof cho một đợt cấp bằng, nhưng chỉ khi triển khai được một cách rõ ràng và không làm app rối.

3. CHƯƠNG 3 – Consensus Protocol, Nodes, Byzantine thinking, PoW/PoS trade-offs
- Không cần xây blockchain public thật như Bitcoin.
- Hệ thống phải thiết kế theo hướng permissioned / consortium / university-trusted network:
  - University Registry
  - Faculty Office
  - Department Office
  - Examination Office
  - QA/Audit Office
- Có khái niệm validator nodes hoặc logical validators ở mức hệ thống.
- Dùng cơ chế “multi-party approval” hoặc “endorsement workflow” mô phỏng consensus trong môi trường đại học.
- Ví dụ:
  - khoa đề xuất cấp chứng chỉ
  - phòng đào tạo phê duyệt
  - registrar ký phát hành
  - hệ thống publish record
- Có thể không implement PoW/PoS thật, nhưng phải phản ánh tư duy consensus:
  - ai có quyền ghi
  - ai có quyền xác nhận
  - ai có quyền đọc
  - làm sao chống sửa đổi đơn phương
- Có dashboard hoặc docs mô tả vì sao bài toán này phù hợp permissioned blockchain hơn permissionless blockchain.

4. CHƯƠNG 4 – Transaction and Transaction Processing
- Mỗi hành động quan trọng phải là một transaction/event:
  - credential request submitted
  - eligibility approved
  - credential issued
  - credential signed
  - credential published
  - credential verified
  - credential revoked
  - credential corrected / superseded
- Mỗi transaction/event phải:
  - có actor
  - có timestamp
  - có entity reference
  - có payload canonical JSON
  - có previous_hash
  - có current_hash
  - có signature/app-signature
  - có validation status
- Có mô hình transaction pipeline:
  - create -> validate -> approve -> commit -> publish
- Có trang explorer cho transaction/ledger events.

5. CHƯƠNG 5 – Contract and Smart Contract
- Hệ thống phải có “smart-contract-like rule engine” hoặc policy engine trong Python.
- Đây không nhất thiết là Solidity thật, nhưng phải phản ánh tư duy:
  - agreed rules
  - hard-coded policies
  - automatic execution by trigger
  - if/then logic
- Ví dụ rules:
  - IF student.completed_all_required_credits AND GPA >= threshold AND tuition_status = cleared AND disciplinary_hold = false
    THEN eligible_for_degree = true
  - IF issuer_approved AND signer_approved
    THEN publish_credential
  - IF fraud_detected OR admin_ordered_revocation
    THEN revoke_credential
- Hệ thống phải có workflow giống smart contract execution:
  - trigger
  - evaluate conditions
  - execute action
  - append transaction to ledger
- Có docs giải thích rõ đâu là smart-contract-like automation, đâu là off-chain business logic.

6. CHƯƠNG 6 – Future of Blockchain, Permissioned vs Permissionless, Use Cases, Digital IDs, Challenges
- Hệ thống phải chọn hướng PRIVATE / PERMISSIONED blockchain-inspired architecture phù hợp với digital IDs / educational credentials.
- Phải thể hiện các yếu tố:
  - authorized participants
  - limited write access
  - public verifiability có kiểm soát
  - privacy-aware data exposure
  - no native currency required
  - possible integration with smart contracts / chaincode-like policy
- Hệ thống phải giải quyết hoặc ít nhất thiết kế để xử lý:
  - scalability
  - privacy
  - security
  - interoperability
  - governance
  - legal / compliance concerns
- Public verification chỉ lộ các trường cần thiết, không lộ dữ liệu riêng tư quá mức.
- Có mô tả vì sao bài toán bằng cấp số phù hợp với blockchain applications như digital IDs / personal identity security / data reporting.

==================================================
II. MỤC TIÊU CUỐI CÙNG CỦA SẢN PHẨM
==================================================

Tạo một hệ thống web cho trường đại học có thể:

- Quản lý tổ chức cấp phát chứng chỉ
- Quản lý sinh viên
- Quản lý chương trình đào tạo
- Quản lý học phần, tín chỉ, kết quả tích lũy
- Quản lý hồ sơ xét điều kiện tốt nghiệp / điều kiện cấp chứng chỉ
- Tạo chứng chỉ số / bằng cấp số / giấy chứng nhận hoàn thành
- Ký số chứng chỉ ở mức ứng dụng
- Ghi record vào ledger chống sửa đổi
- Sinh QR code cho từng chứng chỉ
- Cho phép bên thứ ba kiểm tra tính hợp lệ của chứng chỉ qua public verification page
- Thu hồi / đình chỉ / thay thế chứng chỉ
- Xem timeline, transaction history, audit logs
- Có API
- Có dashboard
- Có role-based access control
- Có báo cáo
- Có Docker
- Có tests
- Có docs đầy đủ

==================================================
III. CÔNG NGHỆ BẮT BUỘC
==================================================

1. Ngôn ngữ chính
- Python

2. Framework backend
- Django

3. API
- Django REST Framework

4. Frontend
- Django Templates + Bootstrap 5 + HTML/CSS/Vanilla JS
- KHÔNG dùng React/Vue/Node build pipeline
- Giao diện tiếng Việt là chính
- Tên code/comment/biến dùng tiếng Anh chuẩn kỹ thuật

5. Database
- Dev: SQLite
- Production-ready: PostgreSQL

6. ORM
- Django ORM

7. Authentication
- Django auth + custom role-based access control

8. File handling
- Upload và quản lý file PDF / ảnh / tài liệu đính kèm

9. QR code
- Python QR code library

10. PDF
- Python PDF generation library để xuất chứng chỉ PDF

11. Hash / signature
- SHA-256
- Dùng thư viện Python cryptography nếu phù hợp để ký số / verify signature
- Có thể dùng RSA hoặc ECDSA ở mức ứng dụng

12. Docker hóa
- Dockerfile
- docker-compose.yml

13. Config
- requirements.txt
- .env.example

14. Logging / security / testing
- logging
- unit tests
- integration tests
- permission tests
- validation tests

==================================================
IV. PHẠM VI NGHIỆP VỤ TOÀN HỆ THỐNG
==================================================

Hệ thống phải hỗ trợ đầy đủ các nghiệp vụ sau:

1. Quản lý tổ chức
- Trường đại học
- Khoa
- Bộ môn
- Phòng đào tạo
- Phòng khảo thí
- Văn phòng registrar
- Đơn vị kiểm định / QA
- Đơn vị đối tác cấp chứng chỉ ngắn hạn
- Có cấp phân quyền theo tổ chức

2. Quản lý người dùng và vai trò
- System Admin
- University Admin
- Registrar
- Faculty Admin
- Department Officer
- Examination Officer
- Academic Advisor
- Signer / Certificate Authority Officer
- Auditor / QA Officer
- Student
- External Verifier (public, không login)
- Organization Staff
- Mỗi role có quyền cụ thể

3. Quản lý sinh viên
- Mã số sinh viên
- Họ tên
- Ngày sinh
- Email
- CCCD / mã định danh nội bộ (nếu cần, có masking)
- Khoa
- Chương trình đào tạo
- Khóa học
- Tình trạng học tập
- Tín chỉ tích lũy
- GPA
- Tuition clearance
- Discipline status
- Graduation status
- Hồ sơ minh chứng

4. Quản lý loại credential
- Degree
- Diploma
- Certificate of Completion
- Transcript Verification Certificate
- Training Certificate
- Short-course Certificate
- Honors / award certificate
- Mỗi loại có template và quy tắc cấp phát riêng

5. Quản lý template chứng chỉ
- Tên mẫu
- Mã mẫu
- Loại chứng chỉ
- Bố cục PDF
- Logo trường
- Chữ ký
- Mã QR
- Dữ liệu hiển thị
- Cấu hình song ngữ Việt/Anh nếu phù hợp

6. Quản lý chương trình đào tạo / điều kiện cấp
- Chương trình
- Danh sách học phần
- Số tín chỉ tối thiểu
- GPA tối thiểu
- Điều kiện bổ sung
- Điều kiện miễn/hoãn
- Quy tắc xét tốt nghiệp
- Chính sách khen thưởng / distinction / honors

7. Hồ sơ yêu cầu cấp chứng chỉ
- Tạo hồ sơ xét cấp
- Gắn với sinh viên
- Loại chứng chỉ
- Nguồn dữ liệu học tập
- Trạng thái workflow
- Người kiểm tra
- Người phê duyệt
- Ghi chú
- Tài liệu đính kèm

8. Quy trình xét duyệt
- Submitted
- Under Review
- Academic Eligible
- Finance Cleared
- Discipline Cleared
- Final Approved
- Signed
- Published
- Rejected
- Revoked
- Superseded
- Có state machine hợp lệ
- Không cho chuyển trạng thái sai

9. Cấp phát chứng chỉ
- Sinh số hiệu chứng chỉ duy nhất
- Sinh mã verification code duy nhất
- Sinh file PDF
- Tính hash payload
- Tính hash file PDF
- Gắn timestamp
- Ký số / application signature
- Ghi ledger event
- Sinh QR code
- Publish public verification page

10. Xác thực công khai
- Public verification by QR
- Public verification by code
- Public verification by certificate ID
- Hiển thị:
  - trạng thái hợp lệ / revoked / superseded / not found
  - tên chứng chỉ
  - tên sinh viên
  - đơn vị cấp
  - ngày cấp
  - số hiệu
  - hash fingerprint rút gọn
  - trạng thái xác thực chữ ký / ledger
- Không lộ dữ liệu nhạy cảm không cần thiết

11. Thu hồi / đình chỉ / thay thế chứng chỉ
- Revoke credential
- Suspend credential
- Re-issue corrected credential
- Mark as superseded
- Ghi lý do
- Ghi quyết định
- Gắn văn bản thu hồi nếu có
- Ledger phải phản ánh đầy đủ lịch sử

12. Audit / compliance
- Audit log
- Ledger explorer
- Verify chain integrity
- Verify signature
- Export audit report
- Track who viewed / who verified if feasible

13. Báo cáo
- Số chứng chỉ đã cấp
- Theo loại
- Theo khoa
- Theo chương trình
- Theo thời gian
- Theo trạng thái
- Số chứng chỉ bị thu hồi
- Số hồ sơ bị từ chối
- Số lần verify công khai
- Export CSV/PDF

==================================================
V. KIẾN TRÚC HỆ THỐNG BẮT BUỘC
==================================================

Thiết kế hệ thống theo kiến trúc rõ ràng, production-minded, nhưng vẫn khả thi cho đồ án.

1. Kiến trúc tổng thể
- Django monolith modular
- Server-rendered frontend
- REST API
- PostgreSQL
- Media storage
- Tamper-evident ledger subsystem
- Policy engine / smart-contract-like rules subsystem
- Verification subsystem
- Notification subsystem (email optional nhưng nên có thiết kế)
- Reporting subsystem

2. Kiến trúc logic theo domain apps
Gợi ý các app Django:

- core
- accounts
- organizations
- students
- academics
- credentials
- issuance
- signatures
- ledger
- verification
- templates_engine
- policy_engine
- audit
- reports
- public_portal
- notifications
- documents

Bạn có thể đổi tên app nhưng phải giữ cấu trúc domain rõ ràng.

3. Mỗi app cần có
- models.py
- views.py
- urls.py
- admin.py
- forms.py nếu cần
- serializers.py nếu có API
- services.py cho business logic
- permissions.py nếu cần
- tests/

==================================================
VI. PERMISSIONED BLOCKCHAIN-INSPIRED LEDGER
==================================================

Đây là phần lõi bắt buộc.

Hệ thống KHÔNG cần triển khai blockchain public thật, nhưng phải xây dựng một lớp ledger chống sửa đổi và có tính chất blockchain-inspired:

1. Mỗi hành động quan trọng phải tạo ledger event
Ví dụ:
- STUDENT_REGISTERED
- PROGRAM_ASSIGNED
- ISSUANCE_REQUEST_CREATED
- ELIGIBILITY_CHECK_PASSED
- ELIGIBILITY_CHECK_FAILED
- APPROVAL_GRANTED
- CREDENTIAL_ISSUED
- PDF_RENDERED
- CREDENTIAL_SIGNED
- CREDENTIAL_PUBLISHED
- CREDENTIAL_VERIFIED
- CREDENTIAL_REVOKED
- CREDENTIAL_SUSPENDED
- CREDENTIAL_SUPERSEDED
- CHAIN_VERIFIED

2. Mỗi ledger event phải có:
- UUID
- sequence_no
- event_type
- entity_type
- entity_id
- actor_user
- actor_organization
- timestamp
- payload_json
- previous_hash
- current_hash
- signature hoặc app_signature
- is_valid
- validation_notes
- optional block_no / batch_no

3. Hashing rules
- current_hash = SHA-256 của:
  sequence_no + timestamp + event_type + entity_type + entity_id + actor identifiers + canonical payload JSON + previous_hash
- Phải có canonical JSON helper
- Phải có utility verify hash
- Không hash kiểu ngẫu hứng

4. Tính bất biến
- Event đã commit thì không cho sửa hoặc xóa từ UI
- Nếu cần sửa sai, phải tạo correction event hoặc superseding event
- Ledger explorer phải nhìn ra toàn bộ chain

5. Verify chain
- Có nút verify chain
- Có management command verify_ledger_integrity
- Có verify theo credential
- Có verify toàn hệ thống
- Nếu phát hiện mismatch:
  - current_hash mismatch
  - previous_hash mismatch
  - signature invalid
  thì báo integrity failure

6. Digital signature
- Mỗi issuer / organization signer có key pair
- Có model quản lý signing key metadata
- Private key không hard-code trong source
- Ưu tiên dùng environment-protected local keys hoặc encrypted storage
- Mỗi credential issuance phải:
  - sign payload hash
  - lưu signature
  - verify được về sau
- Nếu triển khai signing thật quá phức tạp, ít nhất phải có app-level signature/HMAC + architecture docs
- Nhưng ưu tiên làm signing có thật bằng cryptography library

7. Ledger explorer
- Danh sách event
- Filter theo:
  - event type
  - student
  - credential
  - organization
  - date range
- Xem detail:
  - payload
  - current hash
  - previous hash
  - signature status
  - chain link
- Có trang verify chain report

==================================================
VII. SMART-CONTRACT-LIKE POLICY ENGINE
==================================================

Bạn phải tạo một subsystem policy_engine để phản ánh Chương 5.

1. Mục tiêu
- Không cần Solidity
- Nhưng phải có rule engine trong Python
- Có thể hard-code rules hoặc config-driven rules
- Rules phải được thực thi tự động khi có trigger

2. Các rules cần có
- Graduation eligibility rule
- Certificate eligibility rule
- Distinction / honors rule
- Re-issue eligibility rule
- Revoke rule
- Publish rule

3. Ví dụ rule logic
- IF credits_completed >= required_credits AND GPA >= min_gpa AND finance_hold = false AND discipline_hold = false THEN eligible = true
- IF request.status = FINAL_APPROVED AND signer_completed = true THEN issue_and_publish = true
- IF fraud_flag = true OR legal_order = true THEN revoke = true

4. Tính năng
- Evaluate rule
- Store evaluation result
- Explain why passed / failed
- Log to audit and ledger
- Show rule decision in UI
- Trigger automatic state transitions if configured

5. Có mô hình dữ liệu
- PolicyRule
- PolicyEvaluation
- RuleExecutionLog

==================================================
VIII. MÔ HÌNH GIAO DỊCH / TRANSACTION PROCESSING
==================================================

Phải mô hình hóa việc cấp chứng chỉ như transaction processing.

1. Credential issuance transaction pipeline
- Request created
- Evidence attached
- Eligibility checked
- Faculty reviewed
- Registrar approved
- Credential generated
- Payload hashed
- PDF hashed
- Signed
- Published
- Ledger committed
- Public verification enabled

2. Các thành phần transaction
- request_id
- input references:
  - student record
  - program record
  - transcript summary
  - approval record
- output:
  - credential record
  - PDF artifact
  - public verification record
  - ledger entry
  - signature artifact

3. Mỗi transaction phải có:
- initiator
- approver
- validator
- signed proof
- audit trace

4. Có state machine rõ ràng
- Dùng enum/choices
- Validate state transitions

==================================================
IX. MÔ HÌNH DỮ LIỆU CHI TIẾT
==================================================

Thiết kế model tương đối đầy đủ, tối thiểu gồm:

1. User
- custom user hoặc extend profile

2. Organization
- id
- code
- name
- type
- parent_org
- address
- email
- phone
- active
- created_at

3. UserOrganizationRole
- user
- organization
- role
- is_default
- active

4. Student
- student_code
- full_name
- dob
- email
- masked_id_number
- faculty
- department
- program
- cohort
- status
- credits_completed
- gpa
- finance_hold
- discipline_hold
- graduation_eligible
- created_at

5. AcademicProgram
- code
- name
- degree_type
- total_required_credits
- min_gpa
- faculty
- active

6. Course
- code
- name
- credits
- program
- active

7. StudentCourseRecord
- student
- course
- grade
- passed
- term
- year

8. CredentialType
- code
- name
- description
- default_validity_type
- active

9. CredentialTemplate
- code
- name
- credential_type
- version
- template_config_json
- active

10. IssuanceRequest
- request_code
- student
- credential_type
- template
- requested_by
- requested_at
- status
- notes
- evaluation_summary_json

11. ApprovalStep
- request
- step_type
- assigned_to_role
- approved_by
- approved_at
- status
- note

12. PolicyRule
- code
- name
- description
- rule_type
- expression_json hoặc python-safe config
- active

13. PolicyEvaluation
- request
- rule
- result
- detail_json
- executed_at

14. Credential
- credential_code
- serial_number
- verification_code
- student
- credential_type
- template
- issuer_organization
- current_status
- issued_at
- published_at
- revoked_at
- superseded_by
- payload_json
- payload_hash
- pdf_file
- pdf_hash
- qr_image
- signature_value
- signer_name
- signer_title
- ledger_anchor_hash
- public_slug
- notes

15. CredentialVersion
- credential
- version_no
- payload_json
- payload_hash
- pdf_file
- pdf_hash
- created_at

16. SigningKey
- organization
- key_name
- algorithm
- public_key_pem
- private_key_reference
- active
- created_at

17. SignatureRecord
- credential
- signing_key
- signature_algorithm
- signed_payload_hash
- signature_value
- verified
- signed_at

18. VerificationLog
- credential
- verification_method
- requester_ip
- requester_user_agent
- verified_at
- result

19. RevocationRecord
- credential
- reason
- decision_number
- ordered_by
- ordered_at
- public_note
- attachment

20. DocumentAttachment
- entity_type
- entity_id
- file
- uploaded_by
- uploaded_at
- note

21. LedgerEvent
- sequence_no
- event_type
- entity_type
- entity_id
- actor_user
- actor_organization
- payload_json
- previous_hash
- current_hash
- signature
- is_valid
- created_at

22. AuditLog
- user
- action
- object_type
- object_id
- metadata_json
- created_at

==================================================
X. BUSINESS RULES BẮT BUỘC
==================================================

1. student_code, credential_code, serial_number, verification_code phải unique
2. Không cho sửa trực tiếp credential đã publish
3. Nếu cần sửa nội dung, phải tạo version mới hoặc superseding credential
4. Revoked credential vẫn phải verify được nhưng hiển thị trạng thái revoked
5. Public verification page chỉ hiển thị trường đã cho phép
6. Payload phải được canonicalize trước khi hash
7. Mỗi issuance request phải đi qua approval steps hợp lệ
8. Không publish nếu chưa sign
9. Không sign nếu chưa final approved
10. Không revoke nếu user không có quyền
11. Mọi thao tác quan trọng phải ghi cả audit log và ledger event
12. Verify page phải kiểm tra:
    - credential exists
    - status
    - payload hash
    - pdf hash nếu cần
    - signature validity
    - ledger integrity
13. Hỗ trợ masking dữ liệu cá nhân ở public page
14. Có thể cấu hình mức public exposure theo loại credential
15. Có correction event thay vì update silent
16. Có khả năng batch issuance cho nhiều sinh viên trong một đợt

==================================================
XI. QUY TRÌNH NGHIỆP VỤ END-TO-END PHẢI DEMO ĐƯỢC
==================================================

Tạo sẵn dữ liệu demo cho một kịch bản đầy đủ như sau:

Tổ chức:
- Trường Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE)
- Phòng Đào tạo
- Phòng Công tác Sinh viên & Quản lý Văn bằng
- Khoa Công nghệ Thông tin
- Phòng Khảo thí & Đảm bảo chất lượng
- Phòng Kiểm định & Đảm bảo chất lượng

Sinh viên mẫu:
- Nguyễn Thanh Nhật (2001210001)
- Nguyễn Minh Khôi (2001210002)
- Trần Doãn Hòa (2001210003)

Credential types:
- Bằng tốt nghiệp đại học
- Chứng chỉ hoàn thành khóa học blockchain
- Giấy xác nhận tốt nghiệp

Flow demo chuẩn:
1. Admin tạo organization, roles, users
2. Admin tạo academic program
3. Tạo student records và transcript summary
4. Tạo policy rules
5. Faculty officer tạo issuance request cho sinh viên đủ điều kiện
6. Hệ thống evaluate policy rules
7. Examination/finance/discipline clearance được xác nhận
8. Registrar phê duyệt cuối
9. Signer ký chứng chỉ
10. System render PDF + hash payload + hash file + tạo QR
11. Hệ thống commit ledger event chain
12. Credential được publish
13. Người dùng công khai quét QR để verify
14. Auditor chạy verify chain
15. Tạo một case revoke cho một credential
16. Public page hiển thị trạng thái revoked rõ ràng
17. Tạo một case superseded do sai chính tả tên
18. Public page của bản cũ hiển thị superseded, trỏ sang bản mới

Hệ thống phải support đầy đủ flow này bằng UI.

==================================================
XII. GIAO DIỆN WEB CẦN XÂY
==================================================

Thiết kế UI theo phong cách dashboard đại học / hành chính hiện đại, sạch, chuyên nghiệp, responsive.

Cần các trang sau:

1. Authentication
- Login
- Logout
- Change password
- Profile

2. Dashboard
- KPI tổng quan
- Recent issuance requests
- Recent credentials issued
- Pending approvals
- Revoked credentials
- Verification statistics
- Integrity alerts

3. Organization management
- List
- Create
- Detail
- Edit

4. User and role management
- User list
- Assign role
- Membership management

5. Student management
- List
- Create
- Detail
- Academic summary
- Transcript summary
- Eligibility view

6. Program and course management
- Program list
- Program detail
- Course list
- Student academic records

7. Issuance request pages
- List
- Create
- Detail
- Approval workflow view
- Rule evaluation result
- Status transitions

8. Credential pages
- List
- Detail
- Preview
- PDF download
- QR preview
- Version history
- Signature status
- Revoke / supersede actions

9. Policy pages
- Rule list
- Rule detail
- Evaluation logs

10. Ledger pages
- Ledger explorer
- Event detail
- Verify chain page
- Per-credential ledger timeline

11. Verification pages
- Public verify by code
- Public verify by QR
- Public credential status page
- Signature and integrity summary

12. Reports pages
- By faculty
- By credential type
- By date range
- By status
- CSV/PDF export

13. Audit pages
- Audit log list
- Object history
- Integrity issues

Thiết kế template base có:
- sidebar
- topbar
- breadcrumbs
- flash messages
- data tables đẹp
- status badges
- cards
- timeline component
- modal confirm cho actions nguy hiểm

==================================================
XIII. PUBLIC VERIFICATION PORTAL
==================================================

Đây là phần demo rất quan trọng.

Phải có public verification portal, không cần login, hỗ trợ:
- verify bằng QR
- verify bằng verification code
- verify bằng credential code

Public page cần hiển thị:
- Tên credential
- Tên người sở hữu
- Đơn vị cấp
- Ngày cấp
- Trạng thái: valid / revoked / superseded / suspended / not found
- Serial number
- Verification code
- Hash fingerprint rút gọn
- Signature verification status
- Ledger verification status
- Public note nếu revoked hoặc superseded
- Link PDF nếu chính sách cho phép
- Không lộ điểm số chi tiết hoặc thông tin cá nhân nhạy cảm nếu không cần

Phải có giao diện đẹp, thân thiện mobile.

==================================================
XIV. CERTIFICATE PDF RENDERING
==================================================

Hệ thống phải render PDF chứng chỉ thật, không chỉ HTML giả lập.

Mỗi PDF nên có:
- Logo trường
- Tên trường
- Tên chứng chỉ
- Họ tên sinh viên
- Mã sinh viên hoặc masked student code
- Tên chương trình / khóa học
- Ngày cấp
- Số hiệu chứng chỉ
- Chữ ký / tên người ký
- QR verification
- Footer có verification link / code
- Có thể hỗ trợ song ngữ Việt/Anh

Sau khi render PDF:
- tính pdf_hash
- lưu file
- gắn với credential record
- dùng để verify integrity

==================================================
XV. API PHẢI CÓ
==================================================

Tạo REST API tối thiểu cho:
- auth nếu cần
- organizations
- students
- programs
- issuance requests
- approvals
- credentials
- policy evaluations
- verification lookup
- ledger events (read-only)
- audit logs (restricted)
- reports summary

API cần:
- pagination
- filtering
- serializer validation
- permission classes
- consistent response format
- error handling tốt

==================================================
XVI. BẢO MẬT VÀ PHÂN QUYỀN
==================================================

Thiết kế role-based access control rõ ràng:

- System Admin: toàn quyền
- University Admin: quản trị cấp trường
- Faculty Admin: quản trị trong khoa
- Department Officer: xử lý hồ sơ cấp
- Examination Officer: xác nhận dữ liệu học tập
- Registrar: phê duyệt cuối
- Signer: ký chứng chỉ
- Auditor / QA: xem ledger, verify chain, xem audit
- Student: xem credential của mình
- Public: chỉ verify công khai

Yêu cầu bảo mật:
- CSRF protection
- permission checks ở UI và API
- validate file uploads
- secret qua environment variables
- không hard-code private key
- DEBUG off cho production
- cấu hình Django security cơ bản đúng
- mask sensitive personal data
- rate limit public verify nếu khả thi
- secure logging, không log secret

==================================================
XVII. TESTING BẮT BUỘC
==================================================

Viết tests cho ít nhất các luồng sau:

1. Tạo issuance request
2. Rule evaluation pass
3. Rule evaluation fail
4. Approval workflow đúng
5. Không publish khi chưa sign
6. Ký chứng chỉ thành công
7. Verify signature thành công
8. Verify signature fail khi payload bị đổi
9. Ledger chain pass
10. Ledger chain fail nếu dữ liệu bị đổi
11. Public verification trả đúng trạng thái valid
12. Public verification trả đúng trạng thái revoked
13. Superseded credential chuyển hướng logic đúng
14. Permission tests cơ bản
15. PDF hash verify đúng
16. Batch issuance test nếu có

==================================================
XVIII. DEVOPS / TRIỂN KHAI
==================================================

Cần sinh đầy đủ:
- Dockerfile
- docker-compose.yml
- requirements.txt
- .env.example
- README.md
- ARCHITECTURE.md
- API_REFERENCE.md
- TESTING.md
- DEPLOYMENT.md
- THESIS_6_CHAPTER_MAPPING.md

Phải có:
- migrate command
- seed demo data command
- create superuser hướng dẫn
- verify ledger command
- generate sample keys command nếu cần
- runserver hoặc gunicorn config

==================================================
XIX. TÀI LIỆU ĐỒ ÁN GẮN VỚI 6 CHƯƠNG
==================================================

Tạo file THESIS_6_CHAPTER_MAPPING.md trình bày rõ sản phẩm map với chương 1-6 như sau:

- Chương 1:
  Good ledger, ownership, timestamp, description of transaction -> ledger credential issuance
- Chương 2:
  hash, digital signature, timestamped append-only logs, integrity verification
- Chương 3:
  consensus thinking, authorized validators, approval/endorsement workflow, Byzantine-resilient governance mindset
- Chương 4:
  transaction/event model, issuance transaction pipeline, validation flow
- Chương 5:
  smart-contract-like policy engine, automatic if/then credential rules
- Chương 6:
  permissioned architecture, digital IDs, privacy/security/interoperability/governance

==================================================
XX. CẤU TRÚC OUTPUT BẮT BUỘC CỦA BẠN
==================================================

Bạn KHÔNG được chỉ mô tả chung chung.
Bạn phải sinh ra codebase hoàn chỉnh theo từng file.

Thứ tự output bắt buộc:
1. Giới thiệu ngắn về kiến trúc và lý do chọn stack
2. Cây thư mục đầy đủ của project
3. Toàn bộ nội dung từng file quan trọng
4. requirements.txt
5. Dockerfile + docker-compose.yml
6. .env.example
7. README.md
8. docs/*
9. Hướng dẫn chạy local
10. Tài khoản demo và dữ liệu mẫu
11. Cách kiểm thử
12. Cách verify public QR flow

Quy tắc xuất code:
- Mỗi file phải có đường dẫn rõ ràng
- Mỗi file trong một code block riêng
- Không dùng “...” để bỏ đoạn code
- Không nói “chỉ minh họa”
- Không xin xác nhận lại
- Nếu output dài, hãy tự động tiếp tục từ file chưa hoàn thành ở các phần tiếp theo
- Không lặp lại file đã in trước đó

==================================================
XXI. YÊU CẦU VỀ CHẤT LƯỢNG CODE
==================================================

- Code sạch
- Services layer rõ ràng
- Business logic không dồn hết vào views
- Models hợp lý
- Forms/serializers validate tốt
- Permissions rõ ràng
- Logging có cấu trúc
- Errors thân thiện
- UI đẹp, responsive
- Có seed data thực tế
- Có test
- Có docs
- Có production-minded settings

==================================================
XXII. CÁC SERVICES BẮT BUỘC
==================================================

Tạo service layer cho ít nhất các nghiệp vụ:

- create_issuance_request
- evaluate_eligibility_rules
- run_approval_step
- generate_credential_payload
- render_credential_pdf
- compute_payload_hash
- compute_pdf_hash
- sign_credential
- verify_credential_signature
- commit_ledger_event
- verify_ledger_chain
- publish_credential
- revoke_credential
- supersede_credential
- generate_qr_code
- build_public_verification_context
- export_reports

==================================================
XXIII. DỮ LIỆU DEMO BẮT BUỘC
==================================================

Sinh sẵn dữ liệu demo gồm:

Users:
- admin / admin12345
- registrar / registrar12345
- faculty / faculty12345
- signer / signer12345
- auditor / auditor12345
- ntnhat / student12345
- nmkhoi / student12345
- tdhoa / student12345

Organizations:
- Trường Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE)
- Phòng Đào tạo
- Phòng Công tác Sinh viên & Quản lý Văn bằng
- Khoa Công nghệ Thông tin
- Phòng Khảo thí & Đảm bảo chất lượng
- Phòng Kiểm định & Đảm bảo chất lượng

Programs:
- Công nghệ thông tin
- Hệ thống thông tin
- Khoa học dữ liệu

Credential types:
- Bằng tốt nghiệp
- Chứng chỉ hoàn thành khóa học blockchain
- Giấy xác nhận hoàn thành chương trình

Students:
- 2-3 sinh viên đủ điều kiện
- 1 sinh viên chưa đủ điều kiện
- 1 sinh viên có finance hold hoặc discipline hold để test fail rule

Credentials:
- 1 credential valid
- 1 credential revoked
- 1 credential superseded

==================================================
XXIV. KẾT QUẢ CUỐI CÙNG TÔI MONG MUỐN
==================================================

Tôi muốn bạn sinh ra một project Django hoàn chỉnh có thể:
- đăng nhập
- quản lý tổ chức
- quản lý sinh viên
- quản lý chương trình
- xét điều kiện cấp chứng chỉ
- tự động evaluate rules
- phê duyệt nhiều bước
- tạo chứng chỉ PDF
- ký số chứng chỉ
- tạo QR
- publish public verification page
- duy trì ledger hash-chain chống sửa đổi
- verify integrity
- revoke / supersede credential
- có dashboard, báo cáo, API, test, docs, Docker

Bạn phải trả lời như một kỹ sư cao cấp đang trực tiếp code dự án thật.
Không được trả lời chung chung.
Không được bỏ qua file quan trọng.
Không được thu nhỏ thành demo quá tối giản.
Phải bảo đảm MVP mạnh, chạy được, và đủ để đem làm đồ án.

Bắt đầu ngay bây giờ bằng:
1. Chốt kiến trúc
2. In cây thư mục project
3. Sinh toàn bộ code file theo thứ tự hợp lý
4. Sinh docs và hướng dẫn chạy
5. Sinh dữ liệu demo
6. Sinh tests
7. Sinh hướng dẫn verify QR/public flow

Hãy thực hiện toàn bộ.

Continue from the last unfinished file only. Do not repeat previous files. Preserve the same architecture, design language, naming consistency, and documentation quality.