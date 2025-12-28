# Thai DRG Grouper - คู่มือภาษาไทย

🏥 **Thai DRG Grouper** - โปรแกรม DRG Grouper สำหรับประเทศไทย รองรับหลาย version พร้อมกัน

[![PyPI version](https://badge.fury.io/py/thai-drg-grouper.svg)](https://pypi.org/project/thai-drg-grouper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Thai DRG Grouper คืออะไร?

**Thai DRG Grouper** เป็น Python package สำหรับจัดกลุ่ม DRG (Diagnosis Related Group) ของผู้ป่วยในระบบสุขภาพไทย โดยรองรับการใช้งานหลายรูปแบบ:

- 📝 **Python Library** - ใช้งานผ่าน Python code
- 💻 **Command Line (CLI)** - รันผ่าน Terminal/Command Prompt
- 🌐 **REST API** - เรียกใช้ผ่าน HTTP API
- 🐳 **Docker** - รันใน Container

## ✨ ความสามารถหลัก

### 1. รองรับหลาย DRG Versions
```python
# สามารถใช้ DRG หลาย versions พร้อมกัน
manager = ThaiDRGGrouperManager('./data/versions')

# Group ด้วย version 6.3
result_v63 = manager.group('6.3', pdx='J189', los=5)

# Group ด้วย version 5.1
result_v51 = manager.group('5.1', pdx='J189', los=5)

# เปรียบเทียบผลลัพธ์
print(f"v6.3: DRG={result_v63.drg}, RW={result_v63.rw}")
print(f"v5.1: DRG={result_v51.drg}, RW={result_v51.rw}")
```

### 2. ใช้งานได้บนทุก Platform
- ✅ Linux
- ✅ macOS
- ✅ Windows
- ✅ Docker Container

### 3. Batch Processing
ประมวลผลผู้ป่วยหลายรายพร้อมกัน:

```python
# อ่านข้อมูลจาก CSV
import pandas as pd
df = pd.read_csv('patients.csv')

# Group ทุก case
for _, patient in df.iterrows():
    result = manager.group_latest(
        pdx=patient['pdx'],
        sdx=patient['sdx'],
        los=patient['los']
    )
    print(f"{patient['hn']}: DRG={result.drg}")
```

### 4. REST API พร้อมใช้งาน
```bash
# เริ่ม API Server
thai-drg-grouper serve --port 8000

# เรียกใช้ผ่าน API
curl -X POST http://localhost:8000/group \
  -H "Content-Type: application/json" \
  -d '{"pdx": "J189", "sdx": ["E119"], "los": 5}'
```

## 🚀 เริ่มต้นใช้งานอย่างรวดเร็ว

### ติดตั้ง

```bash
# ติดตั้งแบบพื้นฐาน
pip install thai-drg-grouper

# ติดตั้งพร้อม API
pip install thai-drg-grouper[api]

# ติดตั้งแบบครบทุกอย่าง
pip install thai-drg-grouper[all]
```

### ใช้งานแบบง่าย

```python
from thai_drg_grouper import ThaiDRGGrouperManager

# สร้าง manager
manager = ThaiDRGGrouperManager('./data/versions')

# Group ผู้ป่วย
result = manager.group_latest(
    pdx='J189',      # โรคปอดอักเสบ
    sdx=['E119'],    # เบาหวาน
    age=65,
    sex='M',
    los=5
)

# แสดงผลลัพธ์
print(f"DRG: {result.drg}")
print(f"ชื่อ DRG: {result.drg_name}")
print(f"MDC: {result.mdc} - {result.mdc_name}")
print(f"Relative Weight: {result.rw}")
print(f"Adjusted RW: {result.adjrw}")
print(f"PCL (Patient Complexity): {result.pcl}")
```

## 📚 เอกสารประกอบ

- **[การติดตั้ง](getting-started/installation.md)** - วิธีติดตั้งและตั้งค่าเบื้องต้น
- **[คู่มือการใช้งาน](guide/python-library.md)** - วิธีใช้งานโดยละเอียด
- **[ตัวอย่าง](examples/basic.md)** - ตัวอย่างการใช้งานจริง
- **[API Reference](../reference/grouper.md)** - รายละเอียด API แบบเต็ม

## ⚖️ สิทธิ์การรักษาที่รองรับ

- **UC** - บัตรทอง (Universal Coverage)
- **CSMBS** - สิทธิ์ข้าราชการ
- **SSS** - ประกันสังคม

## ⚠️ ข้อควรทราบ

1. **ไม่ใช่โปรแกรม Official** - โปรแกรมนี้ implement จาก DBF files ของ TCMC
2. **ต้อง Validate** - ควรตรวจสอบผลลัพธ์กับโปรแกรม TGrp Official ก่อนใช้งานจริง
3. **ใช้งานทดสอบและวิจัย** - เหมาะสำหรับการเรียนรู้ วิจัย และพัฒนาระบบ

## 💖 สนับสนุนโปรเจกต์นี้

หากคุณเห็นว่าโปรเจกต์นี้มีประโยชน์ เชิญชวนสนับสนุนการพัฒนาด้วยการซื้อกาแฟให้ผู้พัฒนา! ☕

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-ซื้อกาแฟให้-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/sathit)

การสนับสนุนของคุณช่วยให้โปรเจกต์นี้ได้รับการดูแลและพัฒนาต่อไป! 🙏

## 📞 ติดต่อและสนับสนุน

- **GitHub**: [aegisx-platform/thai-drg-grouper](https://github.com/aegisx-platform/thai-drg-grouper)
- **Issues**: [รายงานปัญหา](https://github.com/aegisx-platform/thai-drg-grouper/issues)
- **PyPI**: [thai-drg-grouper](https://pypi.org/project/thai-drg-grouper/)

## 📄 License

MIT License - ใช้งานได้เสรี สามารถดูรายละเอียดได้ที่ [LICENSE](https://github.com/aegisx-platform/thai-drg-grouper/blob/main/LICENSE)
