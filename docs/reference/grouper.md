# Python API Reference

Complete reference for the Thai DRG Grouper Python library.

## Classes

### ThaiDRGGrouperManager

Main manager class for handling multiple DRG versions.

```python
from thai_drg_grouper import ThaiDRGGrouperManager

manager = ThaiDRGGrouperManager(versions_dir='./data/versions')
```

#### Constructor

```python
ThaiDRGGrouperManager(versions_dir: str = './data/versions')
```

**Parameters:**
- `versions_dir` (str): Path to directory containing DRG version data

**Example:**
```python
# Use default directory
manager = ThaiDRGGrouperManager()

# Use custom directory
manager = ThaiDRGGrouperManager('/path/to/versions')
```

#### Methods

##### group_latest()

Group a case using the default/latest DRG version.

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

**Parameters:**
- `pdx` (str, required): Principal diagnosis code (ICD-10-TM)
- `sdx` (List[str], optional): List of secondary diagnosis codes
- `procedures` (List[str], optional): List of ICD-9-CM procedure codes
- `age` (int, optional): Patient age in years (default: 0)
- `sex` (str, optional): Patient sex - 'M' or 'F' (default: 'M')
- `los` (int, optional): Length of stay in days (default: 0)
- `discharge_status` (str, optional): Discharge status code (default: '1')
- `admit_weight` (int, optional): Admission weight in grams for neonates (default: 0)
- `type_in` (str, optional): Type - 'I' (inpatient) or 'O' (outpatient) (default: 'I')
- `datetime_admit` (str, optional): Admission datetime
- `datetime_disch` (str, optional): Discharge datetime

**Returns:**
- `DRGResult`: DRG grouping result

**Example:**
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

Group a case using a specific DRG version.

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

**Parameters:**
- `version` (str, required): DRG version to use (e.g., '6.3', '6.3.4')
- Other parameters: Same as `group_latest()`

**Returns:**
- `DRGResult`: DRG grouping result

**Example:**
```python
# Group with version 6.3
result_v63 = manager.group('6.3', pdx='J189', los=5)

# Group with version 6.3.4
result_v634 = manager.group('6.3.4', pdx='J189', los=5)
```

##### group_all_versions()

Compare DRG grouping across all available versions.

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

**Parameters:**
- Same as `group_latest()`

**Returns:**
- `Dict[str, DRGResult]`: Dictionary mapping version to result

**Example:**
```python
results = manager.group_all_versions(
    pdx='J189',
    sdx=['E119'],
    los=5
)

for version, result in results.items():
    print(f"{version}: DRG={result.drg}, RW={result.rw}")
```

Output:
```
6.3: DRG=04102, RW=1.2345
6.3.4: DRG=04102, RW=1.2500
```

##### list_versions()

Get list of available DRG versions.

```python
list_versions() -> List[str]
```

**Returns:**
- `List[str]`: List of version strings

**Example:**
```python
versions = manager.list_versions()
print(f"Available versions: {versions}")
# Output: Available versions: ['6.3', '6.3.4']
```

##### get_default_version()

Get the default DRG version.

```python
get_default_version() -> str
```

**Returns:**
- `str`: Default version string

**Example:**
```python
default = manager.get_default_version()
print(f"Default version: {default}")
# Output: Default version: 6.3
```

---

### ThaiDRGGrouper

Individual DRG version grouper class.

```python
from thai_drg_grouper import ThaiDRGGrouper

grouper = ThaiDRGGrouper(version_dir='./data/versions/6.3')
```

#### Constructor

```python
ThaiDRGGrouper(version_dir: str)
```

**Parameters:**
- `version_dir` (str): Path to specific version directory

**Example:**
```python
grouper = ThaiDRGGrouper('./data/versions/6.3')
```

#### Methods

##### group()

Group a single case.

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

**Parameters:** Same as `ThaiDRGGrouperManager.group_latest()`

**Returns:**
- `DRGResult`: DRG grouping result

**Example:**
```python
grouper = ThaiDRGGrouper('./data/versions/6.3')
result = grouper.group(pdx='J189', los=5)
```

---

## Data Classes

### DRGResult

Result object containing DRG grouping information.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `drg` | str | DRG code (5 digits) |
| `drg_name` | str | DRG description in Thai |
| `mdc` | str | Major Diagnostic Category (2 digits) |
| `mdc_name` | str | MDC description in Thai |
| `dc` | str | Disease Cluster (4 digits) |
| `dc_name` | str | DC description in Thai |
| `rw` | float | Relative Weight |
| `rw0d` | float | RW for day case |
| `adjrw` | float | Adjusted RW (by LOS) |
| `pcl` | int | Patient Complexity Level (0-4) |
| `is_surgical` | bool | Is surgical DRG |
| `los_status` | str | 'daycase', 'normal', or 'long_stay' |
| `version` | str | DRG version used |

**Example:**
```python
result = manager.group_latest(pdx='J189', los=5)

# Access attributes
print(f"DRG: {result.drg}")                    # 04102
print(f"Name: {result.drg_name}")              # โรคปอด...
print(f"MDC: {result.mdc}")                    # 04
print(f"RW: {result.rw}")                      # 1.2345
print(f"Adjusted RW: {result.adjrw}")          # 1.2345
print(f"PCL: {result.pcl}")                    # 1
print(f"Is Surgical: {result.is_surgical}")    # False
print(f"LOS Status: {result.los_status}")      # normal
print(f"Version: {result.version}")            # 6.3
```

---

## Complete Examples

### Basic Usage

```python
from thai_drg_grouper import ThaiDRGGrouperManager

# Initialize manager
manager = ThaiDRGGrouperManager('./data/versions')

# Simple case
result = manager.group_latest(pdx='J189')
print(f"DRG: {result.drg}, RW: {result.rw}")

# With secondary diagnoses
result = manager.group_latest(
    pdx='J189',
    sdx=['E119', 'I10'],
    age=65,
    sex='M',
    los=5
)
print(f"DRG: {result.drg}, PCL: {result.pcl}")
```

### Surgical Case with Procedures

```python
# Fracture with ORIF surgery
result = manager.group_latest(
    pdx='S82201D',          # Tibial fracture
    sdx=['E119', 'I10'],    # Diabetes, Hypertension
    procedures=['7936'],     # ORIF tibia/fibula
    age=45,
    sex='F',
    los=7
)

print(f"DRG: {result.drg}")              # 08172
print(f"Surgical: {result.is_surgical}") # True
print(f"RW: {result.rw}")                # 5.0602
```

### Version Comparison

```python
# Compare across versions
results = manager.group_all_versions(
    pdx='J189',
    sdx=['E119'],
    los=5
)

# Print comparison
for version, result in results.items():
    print(f"{version}: DRG={result.drg}, RW={result.rw}, PCL={result.pcl}")
```

### Batch Processing

```python
import pandas as pd

# Read patient data
df = pd.read_csv('patients.csv')

# Process all cases
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

# Save results
df_results = pd.DataFrame(results)
df_results.to_csv('drg_results.csv', index=False)
```

### Error Handling

```python
from thai_drg_grouper import ThaiDRGGrouperManager

manager = ThaiDRGGrouperManager()

try:
    # Try to group with invalid version
    result = manager.group('9.9', pdx='J189')
except ValueError as e:
    print(f"Error: {e}")
    # Use default version instead
    result = manager.group_latest(pdx='J189')

try:
    # Try to group without PDX
    result = manager.group_latest(pdx='')
except ValueError as e:
    print(f"Error: Principal diagnosis is required")
```

### Working with Neonates

```python
# Neonate with low birth weight
result = manager.group_latest(
    pdx='P0700',           # Low birth weight
    age=0,
    sex='M',
    los=15,
    admit_weight=1500,     # 1500 grams
    discharge_status='1'
)

print(f"DRG: {result.drg}")
print(f"PCL: {result.pcl}")
```

### Day Case vs Long Stay

```python
# Day case (LOS = 0)
result_day = manager.group_latest(pdx='K358', los=0)
print(f"Day case RW: {result_day.rw0d}")
print(f"Status: {result_day.los_status}")  # daycase

# Normal stay
result_normal = manager.group_latest(pdx='K358', los=3)
print(f"Normal RW: {result_normal.rw}")
print(f"Status: {result_normal.los_status}")  # normal

# Long stay
result_long = manager.group_latest(pdx='K358', los=20)
print(f"Adjusted RW: {result_long.adjrw}")
print(f"Status: {result_long.los_status}")  # long_stay
```

---

## Type Hints

The library is fully typed for better IDE support:

```python
from typing import Optional, List, Dict
from thai_drg_grouper import ThaiDRGGrouperManager, DRGResult

manager: ThaiDRGGrouperManager = ThaiDRGGrouperManager()
result: DRGResult = manager.group_latest(pdx='J189')
versions: List[str] = manager.list_versions()
all_results: Dict[str, DRGResult] = manager.group_all_versions(pdx='J189')
```

---

## See Also

- [REST API Reference](api.md) - HTTP API documentation
- [Examples](../th/examples/basic.md) - More detailed examples in Thai
- [Installation](../getting-started/installation.md) - Setup and configuration
