# REST API Reference

The Thai DRG Grouper REST API provides HTTP endpoints for DRG grouping operations.

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### GET /

Get API information.

**Response:**
```json
{
  "name": "Thai DRG Grouper API",
  "version": "2.0.0",
  "description": "REST API for Thai DRG grouping"
}
```

### GET /versions

List all available DRG versions.

**Response:**
```json
{
  "versions": ["6.3", "6.3.4"],
  "default": "6.3"
}
```

**Example:**
```bash
curl http://localhost:8000/versions
```

### POST /group

Group a case using the default DRG version.

**Request Body:**
```json
{
  "pdx": "string",           // Required: Principal diagnosis (ICD-10)
  "sdx": ["string"],         // Optional: Secondary diagnoses
  "procedures": ["string"],  // Optional: ICD-9-CM procedures
  "age": 0,                  // Optional: Patient age
  "sex": "M",               // Optional: M or F
  "los": 0,                 // Optional: Length of stay (days)
  "discharge_status": "1",  // Optional: Discharge status code
  "admit_weight": 0,        // Optional: Admission weight (grams, for neonates)
  "type_in": "I",          // Optional: I (inpatient) or O (outpatient)
  "datetime_admit": "string", // Optional: Admission datetime
  "datetime_disch": "string"  // Optional: Discharge datetime
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

**Example:**
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

Group a case using a specific DRG version.

**Path Parameters:**
- `version` (string): DRG version (e.g., "6.3", "6.3.4")

**Request Body:** Same as `/group`

**Response:** Same as `/group`

**Example:**
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

Compare DRG grouping results across all available versions.

**Request Body:** Same as `/group`

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

**Example:**
```bash
curl -X POST http://localhost:8000/group/compare \
  -H "Content-Type: application/json" \
  -d '{
    "pdx": "J189",
    "los": 5
  }'
```

### POST /group/batch

Group multiple cases at once.

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
  "version": "6.3"  // Optional: specific version
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

**Example:**
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

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "6.3",
  "versions_available": ["6.3", "6.3.4"]
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

## Response Fields

### DRG Result Object

| Field | Type | Description |
|-------|------|-------------|
| `drg` | string | DRG code (5 digits) |
| `drg_name` | string | DRG description in Thai |
| `mdc` | string | Major Diagnostic Category (2 digits) |
| `mdc_name` | string | MDC description in Thai |
| `dc` | string | Disease Cluster (4 digits) |
| `dc_name` | string | Disease Cluster description |
| `rw` | float | Relative Weight |
| `rw0d` | float | Relative Weight for day case |
| `adjrw` | float | Adjusted RW (based on LOS) |
| `pcl` | integer | Patient Complexity Level (0-4) |
| `is_surgical` | boolean | Is surgical DRG |
| `los_status` | string | `daycase`, `normal`, or `long_stay` |
| `version` | string | DRG version used |

### Patient Complexity Levels (PCL)

| PCL | Description |
|-----|-------------|
| 0 | No complications |
| 1 | Minor complications (CC) |
| 2 | Moderate complications |
| 3 | Major complications (MCC) |
| 4 | Severe complications |

## Error Responses

### 400 Bad Request

Invalid input parameters.

```json
{
  "detail": "Principal diagnosis (pdx) is required"
}
```

### 404 Not Found

Version not found.

```json
{
  "detail": "Version '6.4' not found"
}
```

### 500 Internal Server Error

Server error.

```json
{
  "detail": "Internal server error message"
}
```

## CORS Configuration

The API supports Cross-Origin Resource Sharing (CORS). Configure allowed origins via environment variable:

```bash
CORS_ORIGINS=http://localhost:4200,https://your-app.com
```

Default origins:
- `http://localhost:4200` - Angular development server
- `http://localhost:3000` - React/Vite development server

See [Configuration](../getting-started/installation.md#configuration) for more details.

## Rate Limiting

Currently, there is no rate limiting. Consider implementing rate limiting for production deployments.

## Authentication

The API currently does not require authentication. For production use, consider implementing:
- API key authentication
- JWT tokens
- OAuth 2.0

## Examples

### Python with requests

```python
import requests

# Group a case
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

### JavaScript with fetch

```javascript
// Group a case
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
# Group a case
curl -X POST http://localhost:8000/group \
  -H "Content-Type: application/json" \
  -d '{
    "pdx": "J189",
    "sdx": ["E119", "I10"],
    "age": 65,
    "sex": "M",
    "los": 5
  }'

# Compare versions
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
