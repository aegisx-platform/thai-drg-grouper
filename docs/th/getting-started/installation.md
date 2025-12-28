# การติดตั้ง Thai DRG Grouper

## ความต้องการของระบบ

- Python 3.8 ขึ้นไป
- pip (Python package manager)
- ระบบปฏิบัติการ: Linux, macOS, หรือ Windows

## วิธีติดตั้ง

### 1. ติดตั้งจาก PyPI (แนะนำ)

```bash
# ติดตั้งแบบพื้นฐาน
pip install thai-drg-grouper
```

### 2. ติดตั้งพร้อม Optional Dependencies

#### ติดตั้งพร้อม API Support (FastAPI + Uvicorn)
```bash
pip install thai-drg-grouper[api]
```

#### ติดตั้งพร้อม Development Tools
```bash
pip install thai-drg-grouper[dev]
```

#### ติดตั้งพร้อม Documentation Tools
```bash
pip install thai-drg-grouper[docs]
```

#### ติดตั้งแบบครบทุกอย่าง
```bash
pip install thai-drg-grouper[all]
```

### 3. ติดตั้งจาก Source Code

```bash
# Clone repository
git clone https://github.com/aegisx-platform/thai-drg-grouper.git
cd thai-drg-grouper

# ติดตั้งแบบ development mode
pip install -e .[all]
```

### 4. ติดตั้งผ่าน Docker

```bash
# Pull Docker image จาก GitHub Container Registry
docker pull ghcr.io/aegisx-platform/thai-drg-grouper:latest

# หรือ Build เอง
docker build -t thai-drg-grouper .
```

## ตรวจสอบการติดตั้ง

### ตรวจสอบ Version

```bash
thai-drg-grouper --version
```

### แสดง Help

```bash
thai-drg-grouper --help
```

### ทดสอบ Import

```python
python3 -c "from thai_drg_grouper import ThaiDRGGrouperManager; print('✓ การติดตั้งสำเร็จ!')"
```

## การตั้งค่าข้อมูล DRG Versions

หลังจากติดตั้งแล้ว คุณต้องเพิ่มข้อมูล DRG versions:

### ดาวน์โหลดจาก TCMC

```bash
# แสดง versions ที่สามารถดาวน์โหลดได้
thai-drg-grouper download

# ดาวน์โหลด version 6.3
thai-drg-grouper download --version 6.3 --set-default
```

### เพิ่มจากไฟล์ที่มีอยู่แล้ว

```bash
# เพิ่มจาก zip file
thai-drg-grouper add --version 6.3 --source /path/to/TGrp63.zip --set-default

# เพิ่มจาก folder
thai-drg-grouper add --version 6.3 --source /path/to/TGrp63/ --set-default
```

### ตรวจสอบ Versions ที่ติดตั้ง

```bash
thai-drg-grouper list
```

ผลลัพธ์:
```
Available versions (1):
--------------------------------------------------
  6.3 (default)
    Name: Thai DRG Version 6.3
    Rights: UC, CSMBS, SSS
```

## โครงสร้างไฟล์ข้อมูล

```
data/versions/
├── config.json              # การตั้งค่า default version
├── 6.3/
│   ├── version.json         # ข้อมูล metadata ของ version
│   └── data/
│       ├── c63i10.dbf       # รหัส ICD-10
│       ├── c63proc.dbf      # รหัสหัตถการ
│       ├── c63drg.dbf       # ข้อมูล DRG
│       └── c63ccex.dbf      # กฎ CC Exclusion
└── 6.3.4/
    └── ...
```

## การตั้งค่า (Configuration)

### ตัวแปร Environment Variables

สามารถตั้งค่า API server ผ่าน environment variables โดยสร้างไฟล์ `.env` ในโฟลเดอร์ที่รันโปรแกรม:

```bash
# คัดลอกไฟล์ตัวอย่าง
cp .env.example .env
```

### ตัวเลือกการตั้งค่า

#### การตั้งค่า CORS

กำหนด origins ที่อนุญาตให้เรียก API (คั่นด้วย comma):

```bash
# สำหรับ Development (ค่า default)
CORS_ORIGINS=http://localhost:4200,http://localhost:3000

# สำหรับ Production
CORS_ORIGINS=https://your-app.example.com,https://another-app.example.com
```

**Origins เริ่มต้น:**
- `http://localhost:4200` - Angular development server
- `http://localhost:3000` - React/Vite development server

#### การตั้งค่า Server

```bash
# กำหนด host และ port (ถ้าต้องการ)
HOST=0.0.0.0
PORT=8000
```

### ตัวอย่างไฟล์ .env

```bash
# CORS Configuration
CORS_ORIGINS=http://localhost:4200,http://localhost:3000

# Server Configuration
# HOST=0.0.0.0
# PORT=8000
```

### การใช้งานกับ Docker

เมื่อใช้ Docker สามารถส่ง environment variables ผ่าน `-e` flag:

```bash
docker run -p 8000:8000 \
  -e CORS_ORIGINS="https://your-app.com" \
  ghcr.io/aegisx-platform/thai-drg-grouper:latest
```

หรือใช้ไฟล์ `.env`:

```bash
docker run -p 8000:8000 --env-file .env \
  ghcr.io/aegisx-platform/thai-drg-grouper:latest
```

## การแก้ไขปัญหาที่พบบ่อย

### ปัญหา: ImportError - No module named 'dbfread'

**สาเหตุ:** ไม่ได้ติดตั้ง dependency
**แก้ไข:**
```bash
pip install dbfread
```

### ปัญหา: ไม่พบ data/versions

**สาเหตุ:** ยังไม่ได้ดาวน์โหลดข้อมูล DRG
**แก้ไข:**
```bash
thai-drg-grouper download --version 6.3 --set-default
```

### ปัญหา: Permission denied บน Linux/Mac

**สาเหตุ:** ไม่มีสิทธิ์ติดตั้ง system-wide
**แก้ไข:**
```bash
# ติดตั้งใน user directory
pip install --user thai-drg-grouper

# หรือใช้ virtual environment
python3 -m venv venv
source venv/bin/activate
pip install thai-drg-grouper
```

### ปัญหา: uvicorn: command not found

**สาเหตุ:** ไม่ได้ติดตั้ง API dependencies
**แก้ไข:**
```bash
pip install thai-drg-grouper[api]
```

## ขั้นตอนถัดไป

- 💻 [ตัวอย่างการใช้งาน](../examples/basic.md)
- 🌐 [REST API Reference](../reference/api.md)
- 📚 [Python API Reference](../reference/grouper.md)
