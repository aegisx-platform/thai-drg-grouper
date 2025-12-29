# เอกสาร Python API

เอกสารอ้างอิงฉบับสมบูรณ์สำหรับ Thai DRG Grouper Python library

## Classes

### ThaiDRGGrouperManager

คลาสหลักสำหรับจัดการ DRG หลาย versions

```python
from thai_drg_grouper import ThaiDRGGrouperManager

manager = ThaiDRGGrouperManager(versions_dir='./data/versions')
```

#### Constructor

```python
ThaiDRGGrouperManager(versions_dir: str = './data/versions')
```

**พารามิเตอร์:**
- `versions_dir` (str): path ไปยังโฟลเดอร์ที่เก็บข้อมูล DRG versions

**ตัวอย่าง:**
```python
# ใช้โฟลเดอร์เริ่มต้น
manager = ThaiDRGGrouperManager()

# ใช้โฟลเดอร์ที่กำหนดเอง
manager = ThaiDRGGrouperManager('/path/to/versions')
```

#### Methods

##### group_latest()

จัดกลุ่ม DRG โดยใช้ version เริ่มต้น/ล่าสุด

```python
group_latest(
    pdx: str,
    sdx: Optional[List[str]] = None,
    procedures: Optional[List[str]] = None,
    age: int = 0,
    sex: str = 'M',
    los: int = 0,
    discharge_status: str = '1',
    admit_weight: int = 0,
    type_in: str = 'I',
    datetime_admit: Optional[str] = None,
    datetime_disch: Optional[str] = None
) -> DRGResult
```

**พารามิเตอร์:**
- `pdx` (str, จำเป็น): รหัสโรคหลัก (ICD-10-TM)
- `sdx` (List[str], ตัวเลือก): รายการรหัสโรคร่วม
- `procedures` (List[str], ตัวเลือก): รายการรหัสหัตถการ ICD-9-CM
- `age` (int, ตัวเลือก): อายุผู้ป่วยเป็นปี (default: 0)
- `sex` (str, ตัวเลือก): เพศผู้ป่วย - 'M' หรือ 'F' (default: 'M')
- `los` (int, ตัวเลือก): วันนอน (default: 0)
- `discharge_status` (str, ตัวเลือก): รหัสสถานะจำหน่าย (default: '1')
- `admit_weight` (int, ตัวเลือก): น้ำหนักแรกรับเป็นกรัม สำหรับทารก (default: 0)
- `type_in` (str, ตัวเลือก): ประเภท - 'I' (ผู้ป่วยใน) หรือ 'O' (ผู้ป่วยนอก) (default: 'I')
- `datetime_admit` (str, ตัวเลือก): วันเวลารับ
- `datetime_disch` (str, ตัวเลือก): วันเวลาจำหน่าย

**คืนค่า:**
- `DRGResult`: ผลการจัดกลุ่ม DRG

**ตัวอย่าง:**
```python
result = manager.group_latest(
    pdx='J189',
    sdx=['E119', 'I10'],
    age=65,
    sex='M',
    los=5
)
print(f"DRG: {result.drg}")
print(f"RW: {result.rw}")
```

##### group()

จัดกลุ่ม DRG โดยระบุ version เฉพาะ

```python
group(
    version: str,
    pdx: str,
    sdx: Optional[List[str]] = None,
    procedures: Optional[List[str]] = None,
    age: int = 0,
    sex: str = 'M',
    los: int = 0,
    discharge_status: str = '1',
    admit_weight: int = 0,
    type_in: str = 'I',
    datetime_admit: Optional[str] = None,
    datetime_disch: Optional[str] = None
) -> DRGResult
```

**พารามิเตอร์:**
- `version` (str, จำเป็น): DRG version ที่จะใช้ (เช่น '6.3', '6.3.4')
- พารามิเตอร์อื่นๆ: เหมือนกับ `group_latest()`

**คืนค่า:**
- `DRGResult`: ผลการจัดกลุ่ม DRG

**ตัวอย่าง:**
```python
# จัดกลุ่มด้วย version 6.3
result_v63 = manager.group('6.3', pdx='J189', los=5)

# จัดกลุ่มด้วย version 6.3.4
result_v634 = manager.group('6.3.4', pdx='J189', los=5)
```

##### group_all_versions()

เปรียบเทียบการจัดกลุ่ม DRG ข้าม versions ทั้งหมด

```python
group_all_versions(
    pdx: str,
    sdx: Optional[List[str]] = None,
    procedures: Optional[List[str]] = None,
    age: int = 0,
    sex: str = 'M',
    los: int = 0,
    discharge_status: str = '1',
    admit_weight: int = 0,
    type_in: str = 'I',
    datetime_admit: Optional[str] = None,
    datetime_disch: Optional[str] = None
) -> Dict[str, DRGResult]
```

**พารามิเตอร์:**
- เหมือนกับ `group_latest()`

**คืนค่า:**
- `Dict[str, DRGResult]`: Dictionary ที่มี version เป็น key และผลลัพธ์เป็น value

**ตัวอย่าง:**
```python
results = manager.group_all_versions(
    pdx='J189',
    sdx=['E119'],
    los=5
)

for version, result in results.items():
    print(f"{version}: DRG={result.drg}, RW={result.rw}")
```

ผลลัพธ์:
```
6.3: DRG=04102, RW=1.2345
6.3.4: DRG=04102, RW=1.2500
```

##### list_versions()

ดูรายการ DRG versions ที่มี

```python
list_versions() -> List[str]
```

**คืนค่า:**
- `List[str]`: รายการ version strings

**ตัวอย่าง:**
```python
versions = manager.list_versions()
print(f"Versions ที่มี: {versions}")
# ผลลัพธ์: Versions ที่มี: ['6.3', '6.3.4']
```

##### get_default_version()

ดู DRG version เริ่มต้น

```python
get_default_version() -> str
```

**คืนค่า:**
- `str`: Default version string

**ตัวอย่าง:**
```python
default = manager.get_default_version()
print(f"Version เริ่มต้น: {default}")
# ผลลัพธ์: Version เริ่มต้น: 6.3
```

---

### ThaiDRGGrouper

คลาสสำหรับจัดกลุ่ม DRG version เดียว

```python
from thai_drg_grouper import ThaiDRGGrouper

grouper = ThaiDRGGrouper(version_dir='./data/versions/6.3')
```

#### Constructor

```python
ThaiDRGGrouper(version_dir: str)
```

**พารามิเตอร์:**
- `version_dir` (str): path ไปยังโฟลเดอร์ของ version เฉพาะ

**ตัวอย่าง:**
```python
grouper = ThaiDRGGrouper('./data/versions/6.3')
```

#### Methods

##### group()

จัดกลุ่ม DRG รายเดียว

```python
group(
    pdx: str,
    sdx: Optional[List[str]] = None,
    procedures: Optional[List[str]] = None,
    age: int = 0,
    sex: str = 'M',
    los: int = 0,
    discharge_status: str = '1',
    admit_weight: int = 0,
    type_in: str = 'I',
    datetime_admit: Optional[str] = None,
    datetime_disch: Optional[str] = None
) -> DRGResult
```

**พารามิเตอร์:** เหมือนกับ `ThaiDRGGrouperManager.group_latest()`

**คืนค่า:**
- `DRGResult`: ผลการจัดกลุ่ม DRG

**ตัวอย่าง:**
```python
grouper = ThaiDRGGrouper('./data/versions/6.3')
result = grouper.group(pdx='J189', los=5)
```

---

## Data Classes

### DRGResult

Object ที่เก็บข้อมูลผลการจัดกลุ่ม DRG

**Attributes:**

| Attribute | ชนิด | คำอธิบาย |
|-----------|------|----------|
| `drg` | str | รหัส DRG (5 หลัก) |
| `drg_name` | str | ชื่อ DRG ภาษาไทย |
| `mdc` | str | Major Diagnostic Category (2 หลัก) |
| `mdc_name` | str | ชื่อ MDC ภาษาไทย |
| `dc` | str | Disease Cluster (4 หลัก) |
| `dc_name` | str | ชื่อ DC ภาษาไทย |
| `rw` | float | Relative Weight (น้ำหนักสัมพัทธ์) |
| `rw0d` | float | RW สำหรับ day case |
| `adjrw` | float | Adjusted RW (ปรับตามวันนอน) |
| `pcl` | int | Patient Complexity Level (0-4) |
| `is_surgical` | bool | เป็น DRG ผ่าตัดหรือไม่ |
| `los_status` | str | 'daycase', 'normal', หรือ 'long_stay' |
| `version` | str | DRG version ที่ใช้ |

**ตัวอย่าง:**
```python
result = manager.group_latest(pdx='J189', los=5)

# เข้าถึง attributes
print(f"DRG: {result.drg}")                    # 04102
print(f"ชื่อ: {result.drg_name}")              # โรคปอด...
print(f"MDC: {result.mdc}")                    # 04
print(f"RW: {result.rw}")                      # 1.2345
print(f"Adjusted RW: {result.adjrw}")          # 1.2345
print(f"PCL: {result.pcl}")                    # 1
print(f"ผ่าตัด: {result.is_surgical}")         # False
print(f"สถานะวันนอน: {result.los_status}")     # normal
print(f"Version: {result.version}")            # 6.3
```

---

## ตัวอย่างการใช้งานแบบสมบูรณ์

### การใช้งานพื้นฐาน

```python
from thai_drg_grouper import ThaiDRGGrouperManager

# สร้าง manager
manager = ThaiDRGGrouperManager('./data/versions')

# Case ง่ายๆ
result = manager.group_latest(pdx='J189')
print(f"DRG: {result.drg}, RW: {result.rw}")

# มีโรคร่วม
result = manager.group_latest(
    pdx='J189',
    sdx=['E119', 'I10'],
    age=65,
    sex='M',
    los=5
)
print(f"DRG: {result.drg}, PCL: {result.pcl}")
```

### Case ผ่าตัดพร้อมหัตถการ

```python
# กระดูกหักพร้อมผ่าตัด ORIF
result = manager.group_latest(
    pdx='S82201D',          # กระดูกแข้งหัก
    sdx=['E119', 'I10'],    # เบาหวาน, ความดันโลหิตสูง
    procedures=['7936'],     # ORIF tibia/fibula
    age=45,
    sex='F',
    los=7
)

print(f"DRG: {result.drg}")              # 08172
print(f"ผ่าตัด: {result.is_surgical}")   # True
print(f"RW: {result.rw}")                # 5.0602
```

### เปรียบเทียบ Versions

```python
# เปรียบเทียบข้าม versions
results = manager.group_all_versions(
    pdx='J189',
    sdx=['E119'],
    los=5
)

# แสดงผลเปรียบเทียบ
for version, result in results.items():
    print(f"{version}: DRG={result.drg}, RW={result.rw}, PCL={result.pcl}")
```

### Batch Processing

```python
import pandas as pd

# อ่านข้อมูลผู้ป่วย
df = pd.read_csv('patients.csv')

# ประมวลผลทุก case
results = []
for _, row in df.iterrows():
    result = manager.group_latest(
        pdx=row['pdx'],
        sdx=row['sdx'].split(',') if pd.notna(row['sdx']) else [],
        procedures=row['proc'].split(',') if pd.notna(row['proc']) else [],
        age=row['age'],
        sex=row['sex'],
        los=row['los']
    )
    results.append({
        'hn': row['hn'],
        'drg': result.drg,
        'drg_name': result.drg_name,
        'rw': result.rw,
        'adjrw': result.adjrw
    })

# บันทึกผลลัพธ์
df_results = pd.DataFrame(results)
df_results.to_csv('drg_results.csv', index=False)
```

### การจัดการ Error

```python
from thai_drg_grouper import ThaiDRGGrouperManager

manager = ThaiDRGGrouperManager()

try:
    # ลองใช้ version ที่ไม่มี
    result = manager.group('9.9', pdx='J189')
except ValueError as e:
    print(f"Error: {e}")
    # ใช้ default version แทน
    result = manager.group_latest(pdx='J189')

try:
    # ลองจัดกลุ่มโดยไม่มี PDX
    result = manager.group_latest(pdx='')
except ValueError as e:
    print(f"Error: ต้องระบุรหัสโรคหลัก")
```

### การทำงานกับทารกแรกเกิด

```python
# ทารกน้ำหนักน้อย
result = manager.group_latest(
    pdx='P0700',           # น้ำหนักน้อยมากเมื่อคลอด
    age=0,
    sex='M',
    los=15,
    admit_weight=1500,     # 1500 กรัม
    discharge_status='1'
)

print(f"DRG: {result.drg}")
print(f"PCL: {result.pcl}")
```

### Day Case vs วันนอนยาว

```python
# Day case (LOS = 0)
result_day = manager.group_latest(pdx='K358', los=0)
print(f"Day case RW: {result_day.rw0d}")
print(f"สถานะ: {result_day.los_status}")  # daycase

# วันนอนปกติ
result_normal = manager.group_latest(pdx='K358', los=3)
print(f"Normal RW: {result_normal.rw}")
print(f"สถานะ: {result_normal.los_status}")  # normal

# วันนอนยาว
result_long = manager.group_latest(pdx='K358', los=20)
print(f"Adjusted RW: {result_long.adjrw}")
print(f"สถานะ: {result_long.los_status}")  # long_stay
```

---

## Type Hints

Library รองรับ type hints เต็มรูปแบบสำหรับการใช้งานกับ IDE:

```python
from typing import Optional, List, Dict
from thai_drg_grouper import ThaiDRGGrouperManager, DRGResult

manager: ThaiDRGGrouperManager = ThaiDRGGrouperManager()
result: DRGResult = manager.group_latest(pdx='J189')
versions: List[str] = manager.list_versions()
all_results: Dict[str, DRGResult] = manager.group_all_versions(pdx='J189')
```

---

## ดูเพิ่มเติม

- [เอกสาร REST API](api.md) - เอกสาร HTTP API
- [ตัวอย่างการใช้งาน](../examples/basic.md) - ตัวอย่างโดยละเอียดเพิ่มเติม
- [การติดตั้ง](../getting-started/installation.md) - วิธีติดตั้งและตั้งค่า
