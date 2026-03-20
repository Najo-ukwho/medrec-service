# Medication Reconciliation & Conflict Reporting Service

## Overview

This project is a backend service that helps manage and compare medication lists for patients coming from different sources like clinic EMR, hospital discharge summaries, and patient-reported data.

Since these sources can often conflict, the system stores all versions of medication data and identifies inconsistencies across them.

---

## What this system does

* Accepts medication data from different sources
* Normalizes the data (e.g., formatting, lowercase)
* Stores each update as a new version (instead of overwriting)
* Detects conflicts such as:

  * Same drug with different doses
  * Drugs from conflicting classes
* Stores conflicts and marks them as unresolved
* Allows resolving conflicts with a reason
* Supports filtering conflicts at a clinic level
* Includes test cases and sample dataset generation

---

## How it works (simple flow)

1. A medication list is sent via API
2. Data is normalized
3. A new snapshot is stored (with version number)
4. All previous snapshots for that patient are checked
5. Conflicts are detected
6. Conflicts are stored and can later be resolved

---
## Architecture Overview

The project is structured into three main parts:

- **API Layer** (`routes.py`)  
  Handles incoming requests and responses.

- **Service Layer** (`services/`)  
  Contains business logic such as normalization and conflict detection.

- **Database Layer** (`database.py`)  
  Manages MongoDB connection and data storage.

The flow is:
API → normalization → snapshot storage → conflict detection → conflict storage → response

---
## Data Structure

### Snapshots

Each time data is sent, a new snapshot is created:

```json
{
  "patient_id": "p1",
  "source": "clinic_emr",
  "clinic_id": "clinic_A",
  "medications": [],
  "version": 1,
  "created_at": "timestamp"
}
```

---
## Indexing Strategy

To improve query performance, the following fields are indexed:

- `patient_id` in snapshots and conflicts (for fast lookup per patient)
- `clinic_id` in conflicts (for aggregation queries)
- `status` in conflicts (to filter unresolved conflicts)

These indexes help optimize frequent queries such as:
- fetching patient history
- listing unresolved conflicts
- clinic-based aggregation
```

---
### Conflicts

Conflicts are stored separately:

```json
{
  "patient_id": "p1",
  "clinic_id": "clinic_A",
  "drug": "lisinopril + losartan",
  "type": "class_conflict",
  "status": "unresolved",
  "resolution": {
    "resolved_by": null,
    "reason": null,
    "timestamp": null
  }
}
```

---

## Key Design Choices

* **Versioning instead of updating:**
  Every new input creates a new snapshot. This helps track how data changes over time.

* **Rule-based conflict detection:**
  Conflict rules are stored in a JSON file so they can be modified without changing code.

* **Denormalized storage:**
  Medication lists are stored directly in snapshots for simplicity.

* **Clinic-based tagging:**
  Each record is tagged with a clinic ID to support filtering and reporting.

---

## Assumptions

* Medication names are normalized to lowercase
* Conflict rules are simplified
* No single source is treated as the “truth”
* Conflicts start as unresolved

---

## Limitations

* No real drug database integration
* Time-based aggregation (e.g., last 30 days) is not implemented
* “Stopped medication” conflicts are not handled
* Duplicate conflicts may occur
* Input validation is minimal

---

## How to run locally

1. Clone the repository:

```bash
git clone <repo-url>
cd medrec
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the server:

```bash
uvicorn app.main:app --reload
```

4. Open in browser:

http://127.0.0.1:8000/docs

---

## Database Setup

This project uses MongoDB Atlas (cloud database).

The connection string is already configured in the code.

To use your own database:

* Create a MongoDB Atlas cluster
* Replace the connection string in `database.py`

No local MongoDB installation is required.

**Note:** Credentials are included for evaluation purposes.

---

## Running tests

```bash
# PowerShell (Windows)
$env:PYTHONPATH="."
pytest
```

---

## Seed data

```bash
python scripts/seed.py
```

This generates sample patient data for testing.

---

## API Endpoints

* `POST /patients/{patient_id}/medications` → add medication data
* `GET /patients-with-conflicts` → list patients with conflicts
* `GET /patients-with-conflicts/{clinic_id}` → filter by clinic
* `GET /conflicts/{patient_id}` → view conflicts
* `POST /resolve-conflict/{conflict_id}` → mark conflict as resolved

---

## About AI usage

AI tools were used for:

* initial project scaffolding (FastAPI structure, folder layout)
* debugging environment and setup issues
* generating baseline implementations

All AI-generated code was reviewed, tested, and modified.

### Example of decision-making

* Chose versioned snapshots instead of updating data to preserve history
* Moved conflict rules to a JSON file instead of hardcoding them
* Focused on one aggregation endpoint instead of multiple to stay within scope
* Did not implement “stopped medication” logic due to added complexity

These decisions were made to balance clarity, completeness, and time constraints.

---

## Future Improvements

* Add time-based aggregation (e.g., last 30 days)
* Integrate a real drug interaction database
* Improve validation
* Avoid duplicate conflicts

---

## Demo

After running locally, access:

http://127.0.0.1:8000/docs

Screenshots and screen recordings of key flows are available in the `demo/` folder:
