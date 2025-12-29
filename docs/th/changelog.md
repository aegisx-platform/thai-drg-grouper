# ประวัติการอัพเดท

สำหรับ changelog ฉบับสมบูรณ์ โปรดดูที่: [Changelog (English)](../changelog.md)

## เวอร์ชันล่าสุด

### [2.0.0] - 2024-12-28

#### เพิ่มใหม่
- รองรับ DRG หลาย versions พร้อมกัน พร้อม version manager
- REST API ด้วย FastAPI พร้อม auto-generated documentation
- รองรับ Docker พร้อม multi-platform builds
- CLI ที่ครบครันพร้อมคำสั่ง: list, add, download, remove, group, compare, serve, stats
- รองรับ batch processing
- ฟีเจอร์เปรียบเทียบ versions
- รองรับ cross-platform (Linux, Mac, Windows)
- ตรวจจับไฟล์ DBF อัตโนมัติ
- รองรับกฎ CC/MCC exclusion
- คำนวณ Patient Complexity Level (PCL)
- คำนวณ Adjusted RW ตามวันนอน
- Test suite ที่ครบถ้วน
- CI/CD workflows ด้วย GitHub Actions
- Documentation ด้วย MkDocs Material

#### เปลี่ยนแปลง
- ปรับปรุงโครงสร้างจาก single-version เป็น multi-version
- ปรับปรุงการจัดการ error และ validation
- เพิ่ม type hints และ dataclasses

#### แก้ไข
- การจัดการ encoding ของไฟล์ DBF (Windows-874 สำหรับภาษาไทย)
- การทำให้รหัส ICD-10 เป็นมาตรฐาน
- การค้นหารหัสหัตถการที่รองรับหลายรูปแบบ

---

**หมายเหตุ:** Changelog ฉบับเต็มเป็นภาษาอังกฤษที่ [../changelog.md](../changelog.md)
