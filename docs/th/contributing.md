# การมีส่วนร่วมพัฒนา

ขอบคุณที่สนใจมีส่วนร่วมในการพัฒนา Thai DRG Grouper! เอกสารนี้จะอธิบายแนวทางในการ contribute กับโปรเจกต์

## การเตรียมสภาพแวดล้อมสำหรับพัฒนา

### 1. Fork และ Clone

```bash
git clone https://github.com/YOUR_USERNAME/thai-drg-grouper.git
cd thai-drg-grouper
```

### 2. ติดตั้ง Dependencies

```bash
pip install -e .[all]
```

### 3. รัน Tests

```bash
pytest tests/ -v
```

## ขั้นตอนการพัฒนา

### รูปแบบโค้ด (Code Style)

เราใช้ `black` สำหรับ formatting และ `ruff` สำหรับ linting:

```bash
# Format code
black src/ tests/

# ตรวจสอบ linting
ruff check src/ tests/

# แก้ไข linting issues อัตโนมัติ
ruff check --fix src/ tests/
```

### การเขียน Tests

เขียน tests สำหรับ features ใหม่ทุกอัน:

```bash
# รัน tests ทั้งหมด
pytest

# รันพร้อม coverage
pytest --cov=thai_drg_grouper --cov-report=html

# รัน test เฉพาะ
pytest tests/test_grouper.py::TestGrouper::test_group_fracture -v
```

### การเขียน Documentation

อัพเดท documentation สำหรับ features ใหม่:

```bash
# Build docs ในเครื่อง
mkdocs serve

# เปิดดูที่ http://localhost:8000
```

## ขั้นตอนการส่ง Pull Request

1. **สร้าง Branch**: `git checkout -b feature/your-feature-name`
2. **แก้ไขโค้ด**: ทำตามแนวทาง code style
3. **เพิ่ม Tests**: ตรวจสอบให้แน่ใจว่ามี test coverage
4. **อัพเดท Docs**: เขียน documentation สำหรับ features ใหม่
5. **Commit**: ใช้ commit messages ที่ชัดเจน
6. **Push**: `git push origin feature/your-feature-name`
7. **เปิด PR**: สร้าง pull request บน GitHub

### แนวทางการเขียน Commit Message

ใช้ conventional commits:

- `feat:` Feature ใหม่
- `fix:` แก้ไข Bug
- `docs:` เปลี่ยนแปลง Documentation
- `test:` อัพเดท Tests
- `chore:` งานบำรุงรักษา
- `refactor:` ปรับปรุงโครงสร้างโค้ด

ตัวอย่าง:
```
feat: add support for DRG version 6.5

- เพิ่มการรองรับไฟล์ DBF version 6.5
- อัพเดท logic การตรวจจับ version
- เพิ่ม tests สำหรับ version 6.5
```

## Code Review

การส่ง code ทุกครั้งต้องผ่านการ review เราใช้ GitHub pull requests สำหรับกระบวนการนี้

## การรายงานปัญหา

ใช้ GitHub Issues เพื่อรายงาน bugs หรือขอ features:

- **Bug Report**: อธิบายปัญหา, ขั้นตอนการทำซ้ำ, ผลลัพธ์ที่คาดหวังและผลลัพธ์จริง
- **Feature Request**: อธิบาย feature และ use case
- **Question**: ถามคำถามเกี่ยวกับการใช้งานหรือการ implement

## License

การ contribute หมายความว่าคุณยอมรับให้โค้ดของคุณอยู่ภายใต้ MIT License
