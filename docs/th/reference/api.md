# เอกสาร REST API

REST API ของ Thai DRG Grouper สำหรับการจัดกลุ่ม DRG ผ่าน HTTP endpoints

## Base URL

```
http://localhost:8000
```

## เอกสารแบบ Interactive

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### GET /

ดูข้อมูล API

**Response:**
```json
{
  "name": "Thai DRG Grouper API",
  "version": "2.0.0",
  "description": "REST API for Thai DRG grouping"
}
```

### GET /versions

ดูรายการ DRG versions ที่มี

**Response:**
```json
{
  "versions": ["6.3", "6.3.4"],
  "default": "6.3"
}
```

**ตัวอย่าง:**
```bash
curl http://localhost:8000/versions
```

### POST /group

จัดกลุ่ม DRG โดยใช้ version เริ่มต้น

**Request Body:**
```json
{
  "pdx": "string",           // จำเป็น: รหัสโรคหลัก (ICD-10)
  "sdx": ["string"],         // ตัวเลือก: รหัสโรคร่วม
  "procedures": ["string"],  // ตัวเลือก: รหัสหัตถการ ICD-9-CM
  "age": 0,                  // ตัวเลือก: อายุผู้ป่วย
  "sex": "M",               // ตัวเลือก: M หรือ F
  "los": 0,                 // ตัวเลือก: วันนอน (จำนวนวัน)
  "discharge_status": "1",  // ตัวเลือก: สถานะจำหน่าย
  "admit_weight": 0,        // ตัวเลือก: น้ำหนักแรกรับ (กรัม สำหรับทารก)
  "type_in": "I",          // ตัวเลือก: I (ผู้ป่วยใน) หรือ O (ผู้ป่วยนอก)
  "datetime_admit": "string", // ตัวเลือก: วันเวลารับ
  "datetime_disch": "string"  // ตัวเลือก: วันเวลาจำหน่าย
}
```

**Response:**
```json
{
  "drg": "08172",
  "drg_name": "ผ่าตัดกระดูกและข้อ ระดับความซับซ้อนสูง",
  "mdc": "08",
  "mdc_name": "ระบบโครงกระดูกและกล้ามเนื้อ",
  "dc": "0817",
  "dc_name": "ผ่าตัดกระดูกและข้อ",
  "rw": 5.0602,
  "rw0d": 5.0602,
  "adjrw": 5.0602,
  "pcl": 3,
  "is_surgical": true,
  "los_status": "normal",
  "version": "6.3"
}
```

**ตัวอย่าง:**
```bash
curl -X POST http://localhost:8000/group \
  -H "Content-Type: application/json" \
  -d '{
    "pdx": "S82201D",
    "sdx": ["E119", "I10"],
    "procedures": ["7936"],
    "age": 25,
    "sex": "M",
    "los": 5
  }'
```

### POST /group/{version}

จัดกลุ่ม DRG โดยระบุ version เฉพาะ

**Path Parameters:**
- `version` (string): DRG version (เช่น "6.3", "6.3.4")

**Request Body:** เหมือนกับ `/group`

**Response:** เหมือนกับ `/group`

**ตัวอย่าง:**
```bash
curl -X POST http://localhost:8000/group/6.3 \
  -H "Content-Type: application/json" \
  -d '{
    "pdx": "J189",
    "sdx": ["E119"],
    "los": 5
  }'
```

### POST /group/compare

เปรียบเทียบผลการจัดกลุ่ม DRG ข้าม versions ทั้งหมด

**Request Body:** เหมือนกับ `/group`

**Response:**
```json
{
  "6.3": {
    "drg": "04102",
    "drg_name": "โรคปอด ระดับความซับซ้อนปานกลาง",
    "rw": 1.2345,
    ...
  },
  "6.3.4": {
    "drg": "04102",
    "drg_name": "โรคปอด ระดับความซับซ้อนปานกลาง",
    "rw": 1.2500,
    ...
  }
}
```

**ตัวอย่าง:**
```bash
curl -X POST http://localhost:8000/group/compare \
  -H "Content-Type: application/json" \
  -d '{
    "pdx": "J189",
    "los": 5
  }'
```

### POST /group/batch

จัดกลุ่ม DRG หลายรายพร้อมกัน

**Request Body:**
```json
{
  "cases": [
    {
      "pdx": "string",
      "sdx": ["string"],
      "procedures": ["string"],
      "age": 0,
      "sex": "M",
      "los": 0
    }
  ],
  "version": "6.3"  // ตัวเลือก: version เฉพาะ
}
```

**Response:**
```json
{
  "results": [
    {
      "drg": "08172",
      "drg_name": "...",
      ...
    }
  ]
}
```

**ตัวอย่าง:**
```bash
curl -X POST http://localhost:8000/group/batch \
  -H "Content-Type: application/json" \
  -d '{
    "cases": [
      {"pdx": "J189", "los": 5},
      {"pdx": "S82201D", "procedures": ["7936"], "los": 7}
    ]
  }'
```

### GET /health

ตรวจสอบสถานะ API

**Response:**
```json
{
  "status": "healthy",
  "version": "6.3",
  "versions_available": ["6.3", "6.3.4"]
}
```

**ตัวอย่าง:**
```bash
curl http://localhost:8000/health
```

## ฟิลด์ใน Response

### DRG Result Object

| ฟิลด์ | ชนิด | คำอธิบาย |
|-------|------|----------|
| `drg` | string | รหัส DRG (5 หลัก) |
| `drg_name` | string | ชื่อ DRG ภาษาไทย |
| `mdc` | string | Major Diagnostic Category (2 หลัก) |
| `mdc_name` | string | ชื่อ MDC ภาษาไทย |
| `dc` | string | Disease Cluster (4 หลัก) |
| `dc_name` | string | ชื่อ Disease Cluster |
| `rw` | float | Relative Weight (น้ำหนักสัมพัทธ์) |
| `rw0d` | float | Relative Weight สำหรับ day case |
| `adjrw` | float | Adjusted RW (ปรับตามวันนอน) |
| `pcl` | integer | Patient Complexity Level (0-4) |
| `is_surgical` | boolean | เป็น DRG ผ่าตัดหรือไม่ |
| `los_status` | string | `daycase`, `normal`, หรือ `long_stay` |
| `version` | string | DRG version ที่ใช้ |

### ระดับความซับซ้อนผู้ป่วย (PCL)

| PCL | คำอธิบาย |
|-----|----------|
| 0 | ไม่มีภาวะแทรกซ้อน |
| 1 | มีภาวะแทรกซ้อนเล็กน้อย (CC) |
| 2 | มีภาวะแทรกซ้อนปานกลาง |
| 3 | มีภาวะแทรกซ้อนมาก (MCC) |
| 4 | มีภาวะแทรกซ้อนรุนแรง |

## Error Responses

### 400 Bad Request

พารามิเตอร์ไม่ถูกต้อง

```json
{
  "detail": "Principal diagnosis (pdx) is required"
}
```

### 404 Not Found

ไม่พบ version ที่ระบุ

```json
{
  "detail": "Version '6.4' not found"
}
```

### 500 Internal Server Error

ข้อผิดพลาดของเซิร์ฟเวอร์

```json
{
  "detail": "Internal server error message"
}
```

## การตั้งค่า CORS

API รองรับ Cross-Origin Resource Sharing (CORS) สามารถกำหนด origins ที่อนุญาตผ่าน environment variable:

```bash
CORS_ORIGINS=http://localhost:4200,https://your-app.com
```

Origins เริ่มต้น:
- `http://localhost:4200` - Angular development server
- `http://localhost:3000` - React/Vite development server

ดูรายละเอียดเพิ่มเติมที่ [การตั้งค่า](../getting-started/installation.md#การตั้งค่า-configuration)

## Rate Limiting

ปัจจุบันยังไม่มี rate limiting หากนำไปใช้งานจริง แนะนำให้เพิ่ม rate limiting

## Authentication

API ปัจจุบันไม่ต้องการการ authenticate สำหรับการใช้งานจริง แนะนำให้เพิ่ม:
- API key authentication
- JWT tokens
- OAuth 2.0

## ตัวอย่างการใช้งาน

### Python กับ requests

```python
import requests

# จัดกลุ่ม DRG
response = requests.post(
    "http://localhost:8000/group",
    json={
        "pdx": "J189",
        "sdx": ["E119", "I10"],
        "age": 65,
        "sex": "M",
        "los": 5
    }
)
result = response.json()
print(f"DRG: {result['drg']}, RW: {result['rw']}")
```

### JavaScript กับ fetch

```javascript
// จัดกลุ่ม DRG
const response = await fetch('http://localhost:8000/group', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    pdx: 'J189',
    sdx: ['E119', 'I10'],
    age: 65,
    sex: 'M',
    los: 5
  })
});
const result = await response.json();
console.log(`DRG: ${result.drg}, RW: ${result.rw}`);
```

### cURL

```bash
# จัดกลุ่ม DRG
curl -X POST http://localhost:8000/group \
  -H "Content-Type: application/json" \
  -d '{
    "pdx": "J189",
    "sdx": ["E119", "I10"],
    "age": 65,
    "sex": "M",
    "los": 5
  }'

# เปรียบเทียบ versions
curl -X POST http://localhost:8000/group/compare \
  -H "Content-Type: application/json" \
  -d '{"pdx": "J189", "los": 5}'

# Batch processing
curl -X POST http://localhost:8000/group/batch \
  -H "Content-Type: application/json" \
  -d '{
    "cases": [
      {"pdx": "J189", "los": 5},
      {"pdx": "S82201D", "procedures": ["7936"], "los": 7}
    ]
  }'
```
