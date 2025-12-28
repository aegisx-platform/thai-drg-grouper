# ตัวอย่างการใช้งานพื้นฐาน

## ตัวอย่างที่ 1: Group ผู้ป่วยรายเดียว (Single Case)

### โรคปอดอักเสบ (Pneumonia)

```python
from thai_drg_grouper import ThaiDRGGrouperManager

# สร้าง manager
manager = ThaiDRGGrouperManager('./data/versions')

# ข้อมูลผู้ป่วย
result = manager.group_latest(
    pdx='J189',      # Pneumonia, unspecified organism
    sdx=['E119'],    # Type 2 diabetes mellitus
    age=65,
    sex='M',
    los=5           # Length of stay = 5 วัน
)

# แสดงผลลัพธ์
print(f"DRG Code: {result.drg}")
print(f"DRG Name: {result.drg_name}")
print(f"MDC: {result.mdc} - {result.mdc_name}")
print(f"Relative Weight: {result.rw}")
print(f"Adjusted RW: {result.adjrw}")
print(f"PCL: {result.pcl}")
print(f"ประเภท: {'ผ่าตัด' if result.is_surgical else 'รักษาทั่วไป'}")
```

**ผลลัพธ์:**
```
DRG Code: 04523
DRG Name: Respiratory infection/inflammation w maj CCC
MDC: 04 - Diseases & Disorders of the Respiratory System
Relative Weight: 3.1233
Adjusted RW: 3.1233
PCL: 3
ประเภท: รักษาทั่วไป
```

---

## ตัวอย่างที่ 2: กระดูกหัก + ผ่าตัด (Fracture with Surgery)

```python
result = manager.group_latest(
    pdx='S82201D',           # Fracture of tibia
    sdx=['E119', 'I10'],     # Diabetes + Hypertension
    procedures=['7936'],     # Open reduction of fracture
    age=45,
    sex='M',
    los=7
)

print(f"DRG: {result.drg}")
print(f"RW: {result.rw}")
print(f"Adj RW: {result.adjrw}")
print(f"มี OR Procedure: {result.has_or_procedure}")
print(f"PCL: {result.pcl}")
print(f"CC: {len(result.cc_list)}, MCC: {len(result.mcc_list)}")
```

**ผลลัพธ์:**
```
DRG: 08173
RW: 8.8892
Adj RW: 8.8892
มี OR Procedure: True
PCL: 4
CC: 1, MCC: 1
```

---

## ตัวอย่างที่ 3: เปรียบเทียบ DRG Versions

```python
# เปรียบเทียบผลลัพธ์ระหว่าง version 5.1 และ 6.3
results = manager.group_all_versions(
    pdx='S82201D',
    sdx=['E119'],
    los=7
)

print("เปรียบเทียบ DRG Versions:")
print("-" * 50)
for version, result in results.items():
    if result:
        print(f"Version {version}:")
        print(f"  DRG: {result.drg}")
        print(f"  RW: {result.rw}")
        print(f"  Adj RW: {result.adjrw}")
        print()
```

---

## ตัวอย่างที่ 4: Batch Processing

### วิธีที่ 1: อ่านจาก CSV

```python
import pandas as pd

# อ่านข้อมูลผู้ป่วย
df = pd.read_csv('patients.csv')

# ตัวอย่าง patients.csv:
# hn,pdx,sdx,procedures,age,sex,los
# 001,J189,E119,,65,M,5
# 002,S82201D,"E119,I10",7936,45,M,7
# 003,I219,,,55,F,3

# ประมวลผลทุก case
results = []
for _, patient in df.iterrows():
    # แปลง sdx และ procedures จาก string เป็น list
    sdx = patient['sdx'].split(',') if pd.notna(patient['sdx']) else []
    procedures = patient['procedures'].split(',') if pd.notna(patient['procedures']) else []

    # Group
    result = manager.group_latest(
        pdx=patient['pdx'],
        sdx=sdx,
        procedures=procedures,
        age=int(patient['age']),
        sex=patient['sex'],
        los=int(patient['los'])
    )

    # เก็บผลลัพธ์
    results.append({
        'hn': patient['hn'],
        'drg': result.drg,
        'drg_name': result.drg_name,
        'rw': result.rw,
        'adjrw': result.adjrw,
        'pcl': result.pcl
    })

# บันทึกผลลัพธ์
results_df = pd.DataFrame(results)
results_df.to_csv('drg_results.csv', index=False)

print(f"ประมวลผล {len(results)} cases เสร็จสิ้น")
print(f"Total RW: {results_df['rw'].sum():.2f}")
print(f"Average RW: {results_df['rw'].mean():.2f}")
```

### วิธีที่ 2: ใช้ Function

```python
def batch_group(cases):
    """
    Group หลาย cases พร้อมกัน

    Args:
        cases: list of dict containing patient data

    Returns:
        list of results
    """
    results = []
    for case in cases:
        result = manager.group_latest(**case)
        results.append({
            'drg': result.drg,
            'rw': result.rw,
            'adjrw': result.adjrw,
            'pcl': result.pcl
        })
    return results

# ใช้งาน
cases = [
    {'pdx': 'J189', 'sdx': ['E119'], 'age': 65, 'sex': 'M', 'los': 5},
    {'pdx': 'I219', 'age': 55, 'sex': 'F', 'los': 3},
    {'pdx': 'S82201D', 'sdx': ['E119'], 'procedures': ['7936'], 'age': 45, 'sex': 'M', 'los': 7}
]

results = batch_group(cases)
for i, r in enumerate(results, 1):
    print(f"Case {i}: DRG={r['drg']}, RW={r['rw']}")
```

---

## ตัวอย่างที่ 5: ใช้งานผ่าน REST API

### เริ่ม API Server

```bash
# วิธีที่ 1: ใช้ CLI
thai-drg-grouper serve --port 8000

# วิธีที่ 2: ใช้ uvicorn
uvicorn thai_drg_grouper.api:app --port 8000 --reload

# วิธีที่ 3: ใช้ Docker
docker run -p 8000:8000 ghcr.io/aegisx-platform/thai-drg-grouper:latest
```

### เรียกใช้ API

#### Python (requests)
```python
import requests
import json

# Group single case
response = requests.post(
    'http://localhost:8000/group',
    json={
        'pdx': 'J189',
        'sdx': ['E119'],
        'age': 65,
        'sex': 'M',
        'los': 5
    }
)

result = response.json()
print(f"DRG: {result['drg']}")
print(f"RW: {result['rw']}")
```

#### curl
```bash
# Group single case
curl -X POST http://localhost:8000/group \
  -H "Content-Type: application/json" \
  -d '{
    "pdx": "J189",
    "sdx": ["E119"],
    "age": 65,
    "sex": "M",
    "los": 5
  }'

# แสดง versions
curl http://localhost:8000/versions

# Health check
curl http://localhost:8000/health
```

---

## ตัวอย่างที่ 6: ตรวจสอบความถูกต้อง

```python
result = manager.group_latest(
    pdx='J189',
    sdx=['E119'],
    age=65,
    sex='M',
    los=5
)

# ตรวจสอบว่า group สำเร็จหรือไม่
if result.is_valid:
    print(f"✓ Group สำเร็จ: DRG={result.drg}")
else:
    print("✗ เกิดข้อผิดพลาด:")
    for error in result.errors:
        print(f"  - {error}")

    # คำเตือน (ถ้ามี)
    if result.warnings:
        print("คำเตือน:")
        for warning in result.warnings:
            print(f"  - {warning}")
```

---

## ตัวอย่างที่ 7: ดูข้อมูลสถิติ

```python
# ดูสถิติของ version ที่ติดตั้ง
stats = manager.get_stats('6.3')

print(f"DRG Version: {stats['version']}")
print(f"จำนวนรหัส ICD-10: {stats['icd10_count']:,}")
print(f"จำนวนรหัสหัตถการ: {stats['procedure_count']:,}")
print(f"จำนวน Disease Cluster: {stats['dc_count']:,}")
print(f"จำนวน DRG: {stats['drg_count']:,}")
print(f"จำนวนกฎ CC Exclusion: {stats['cc_exclusion_count']:,}")
```

**ผลลัพธ์:**
```
DRG Version: 6.3
จำนวนรหัส ICD-10: 15,109
จำนวนรหัสหัตถการ: 7,695
จำนวน Disease Cluster: 605
จำนวน DRG: 1,546
จำนวนกฎ CC Exclusion: 1,916
```

---

## ตัวอย่างที่ 8: การจัดการ Versions

```python
# แสดง versions ทั้งหมด
versions = manager.list_versions()
for v in versions:
    print(f"Version: {v.version}")
    print(f"  Name: {v.name}")
    print(f"  Release Date: {v.release_date}")
    print(f"  Default: {v.is_default}")
    print(f"  Rights: {', '.join(v.rights)}")
    print()

# เปลี่ยน default version
manager.set_default_version('6.3')

# ตรวจสอบ default version
default = manager.get_default_version()
print(f"Default version: {default}")
```

---

## ตัวอย่างที่ 9: แสดงผลลัพธ์แบบละเอียด

```python
def print_result_detailed(result):
    """แสดงผลลัพธ์แบบละเอียด"""
    print("=" * 60)
    print("ผลการ Group DRG")
    print("=" * 60)
    print(f"\n📋 ข้อมูลพื้นฐาน")
    print(f"  PDx: {result.pdx}")
    print(f"  SDx: {', '.join(result.sdx) if result.sdx else '-'}")
    print(f"  Procedures: {', '.join(result.procedures) if result.procedures else '-'}")
    print(f"  อายุ: {result.age} ปี")
    print(f"  เพศ: {result.sex}")
    print(f"  LOS: {result.los} วัน")

    print(f"\n🏥 ผลลัพธ์ DRG")
    print(f"  DRG Code: {result.drg}")
    print(f"  DRG Name: {result.drg_name}")
    print(f"  MDC: {result.mdc} - {result.mdc_name}")
    print(f"  Disease Cluster: {result.dc}")

    print(f"\n💰 Relative Weight")
    print(f"  RW: {result.rw}")
    print(f"  RW (0 day): {result.rw0d}")
    print(f"  Adjusted RW: {result.adjrw}")
    print(f"  LOS Status: {result.los_status}")

    print(f"\n🎯 Patient Complexity")
    print(f"  PCL: {result.pcl}")
    print(f"  CC: {len(result.cc_list)}")
    print(f"  MCC: {len(result.mcc_list)}")
    if result.cc_list:
        print(f"  CC List: {', '.join(result.cc_list)}")
    if result.mcc_list:
        print(f"  MCC List: {', '.join(result.mcc_list)}")

    print(f"\n⚕️  ประเภทการรักษา")
    print(f"  มี OR Procedure: {'ใช่' if result.has_or_procedure else 'ไม่'}")
    print(f"  ผ่าตัด: {'ใช่' if result.is_surgical else 'ไม่'}")

    print(f"\n✅ สถานะ")
    print(f"  Valid: {result.is_valid}")
    if result.errors:
        print(f"  Errors: {', '.join(result.errors)}")
    if result.warnings:
        print(f"  Warnings: {', '.join(result.warnings)}")

    print("=" * 60)

# ใช้งาน
result = manager.group_latest(pdx='J189', sdx=['E119'], age=65, sex='M', los=5)
print_result_detailed(result)
```

---

## ตัวอย่างที่ 10: Integration กับระบบ HIS

```python
class DRGService:
    """Service สำหรับ integrate กับระบบ HIS"""

    def __init__(self, versions_path='./data/versions'):
        self.manager = ThaiDRGGrouperManager(versions_path)

    def group_admission(self, admission_data):
        """
        Group จากข้อมูล admission

        Args:
            admission_data: dict มีข้อมูล AN, HN, PDx, SDx, etc.

        Returns:
            dict: ผลลัพธ์ DRG
        """
        result = self.manager.group_latest(
            pdx=admission_data['pdx'],
            sdx=admission_data.get('sdx', []),
            procedures=admission_data.get('procedures', []),
            age=admission_data['age'],
            sex=admission_data['sex'],
            los=admission_data['los']
        )

        return {
            'an': admission_data['an'],
            'hn': admission_data['hn'],
            'drg': result.drg,
            'drg_name': result.drg_name,
            'rw': result.rw,
            'adjrw': result.adjrw,
            'pcl': result.pcl,
            'is_valid': result.is_valid,
            'grouped_at': result.grouped_at
        }

    def batch_group_admissions(self, admissions):
        """Group หลาย admissions"""
        return [self.group_admission(adm) for adm in admissions]

# ใช้งาน
service = DRGService()

admission = {
    'an': '67001234',
    'hn': '1234567',
    'pdx': 'J189',
    'sdx': ['E119'],
    'age': 65,
    'sex': 'M',
    'los': 5
}

result = service.group_admission(admission)
print(f"AN: {result['an']}, DRG: {result['drg']}, RW: {result['rw']}")
```

---

## ข้อแนะนำในการใช้งาน

1. **ตรวจสอบความถูกต้อง**: ควรตรวจสอบ `result.is_valid` ทุกครั้ง
2. **จัดการ Error**: ตรวจสอบ `result.errors` และ `result.warnings`
3. **ใช้ Version ที่เหมาะสม**: เลือกใช้ DRG version ที่ตรงกับช่วงเวลาที่รักษา
4. **Validate กับ Official**: ควรเทียบผลลัพธ์กับโปรแกรม TGrp Official
5. **Batch Processing**: สำหรับข้อมูลจำนวนมาก ควรใช้ batch processing เพื่อประสิทธิภาพ

---

## ดูเพิ่มเติม

- [คู่มือ Python Library](../guide/python-library.md)
- [คู่มือ REST API](../guide/api.md)
- [คู่มือ CLI](../guide/cli.md)
