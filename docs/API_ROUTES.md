# API Routes Guide

The API now provides separate, dedicated routes for each classification type, making it clearer and easier to understand
which endpoint to use.

## Overview

The API supports a **two-stage classification workflow**:

1. **Stage 1**: Classify a complaint as either an **Adverse Event** or **Product Complaint**
2. **Stage 2**: Further classify into specific categories based on the type:
   - **Adverse Events** → Medical categories (e.g., Gastrointestinal, Pancreatitis)
   - **Product Complaints** → Quality/defect categories (e.g., Device malfunction, Packaging defect)

---

## Endpoints

### System Endpoints

#### `GET /`

Root endpoint that shows API information and available endpoints.

**Response:**

```json
{
  "name": "DSPy Complaint Classifier API",
  "version": "0.3.0",
  "status": "running",
  "docs": "/docs",
  "redoc": "/redoc",
  "health": "/health",
  "endpoints": {
    "ae_pc": "/classify/ae-pc",
    "ae_category": "/classify/ae-category",
    "pc_category": "/classify/pc-category"
  }
}
```

#### `GET /health`

Check the health status of all classifiers.

**Response:**

```json
{
  "status": "ok",
  "classifiers": {
    "ae-pc": "ok",
    "ae-category": "ok",
    "pc-category": "ok"
  }
}
```

---

### Classification Endpoints

#### `POST /classify/ae-pc`

**Stage 1: Classify as Adverse Event or Product Complaint**

Determines whether a complaint is a medical/health issue (Adverse Event) or a quality/defect issue (Product Complaint).

**Request:**

```json
{
  "complaint": "I experienced severe nausea and vomiting after taking Ozempic."
}
```

**Response:**

```json
{
  "classification": "Adverse Event",
  "justification": "The complaint describes medical symptoms (nausea and vomiting) following medication use, which is a health-related issue.",
  "classification_type": "ae-pc"
}
```

#### `POST /classify/ae-category`

**Stage 2: Classify Adverse Event into medical category**

For complaints identified as Adverse Events, this classifies them into specific medical categories.

**Possible Categories:**

- Gastrointestinal disorders
- Pancreatitis
- Hepatobiliary (gallbladder) disease
- Hypoglycemia
- Eye disorders (Diabetic retinopathy complications)
- Renal events (Acute kidney injury)
- Hypersensitivity
- Injection-site reactions
- Cardiovascular signs
- Peri-procedural aspiration risk
- Gastrointestinal disorders (Gastroparesis)

**Request:**

```json
{
  "complaint": "I developed pancreatitis after using Ozempic for 3 months."
}
```

**Response:**

```json
{
  "classification": "Pancreatitis",
  "justification": "The complaint explicitly mentions pancreatitis, which is a known adverse event category for this medication.",
  "classification_type": "ae-category"
}
```

#### `POST /classify/pc-category`

**Stage 2: Classify Product Complaint into quality/defect category**

For complaints identified as Product Complaints, this classifies them into specific quality/defect categories.

**Possible Categories:**

- Stability/Appearance defect
- Device malfunction
- Storage/Temperature excursion
- Labeling error
- Contamination/Foreign matter
- Packaging defect
- Counterfeit/Unauthorized source
- Potency/Assay defect
- Distribution/Expiry

**Request:**

```json
{
  "complaint": "The medication arrived warm, temperature control was not maintained during shipping."
}
```

**Response:**

```json
{
  "classification": "Storage/Temperature excursion",
  "justification": "The complaint indicates temperature control issues during shipping, which falls under storage and temperature excursion problems.",
  "classification_type": "pc-category"
}
```

---

## Example Workflow

Here's a typical two-stage classification workflow:

### 1. First, classify as AE or PC

```bash
curl -X POST "http://localhost:8000/classify/ae-pc" \
  -H "Content-Type: application/json" \
  -d '{
    "complaint": "My Ozempic pen arrived with a cracked cartridge and leaked everywhere."
  }'
```

**Response:**

```json
{
  "classification": "Product Complaint",
  "justification": "The issue describes a physical defect with the pen device, not a health-related symptom.",
  "classification_type": "ae-pc"
}
```

### 2. Then, classify into specific category

Since it's a Product Complaint, use the `/classify/pc-category` endpoint:

```bash
curl -X POST "http://localhost:8000/classify/pc-category" \
  -H "Content-Type: application/json" \
  -d '{
    "complaint": "My Ozempic pen arrived with a cracked cartridge and leaked everywhere."
  }'
```

**Response:**

```json
{
  "classification": "Device malfunction",
  "justification": "The cracked cartridge and leaking represent a mechanical failure of the pen device.",
  "classification_type": "pc-category"
}
```

---

## Interactive Documentation

- **Swagger UI**: Visit `/docs` for interactive API documentation
- **ReDoc**: Visit `/redoc` for alternative documentation format

Both interfaces allow you to test the endpoints directly from your browser.

---

## Error Handling

All endpoints return standard HTTP status codes:

- `200`: Success
- `503`: Service Unavailable (classifier not loaded or artifact missing)

**Example Error Response:**

```json
{
  "detail": "AE-PC classifier unavailable: Classifier artifact not loaded"
}
```
