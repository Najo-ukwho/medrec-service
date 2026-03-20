from fastapi import APIRouter
from app.database import db
from app.services.normalization import normalize_medication
from app.services.conflict_detection import detect_conflicts
from datetime import datetime

router = APIRouter()


@router.post("/patients/{patient_id}/medications")
def ingest_medications(patient_id: str, data: dict):

    #  Step 1: Normalize medications
    normalized_meds = [
        normalize_medication(m)
        for m in data.get("medications", [])
    ]

    #  Step 2: Compute version
    existing_count = db.snapshots.count_documents({"patient_id": patient_id})

    record = {
        "patient_id": patient_id,
        "source": data.get("source"),
        "medications": normalized_meds,
        "clinic_id": data.get("clinic_id", "clinic_1"), 
        "version": existing_count + 1,
        "created_at": datetime.utcnow()
    }

    #  Step 3: Store snapshot
    db.snapshots.insert_one(record)

    #  Step 4: Fetch all snapshots
    snapshots = list(db.snapshots.find({"patient_id": patient_id}))

    #  Step 5: Detect conflicts
    conflicts = detect_conflicts(snapshots)

    #  Step 6: Store conflicts
    for c in conflicts:
        db.conflicts.insert_one({
            "patient_id": patient_id,
            "clinic_id": record["clinic_id"],  
            "drug": c["drug"],
            "type": c["type"],
            "details": c["details"],
            "status": "unresolved",
            "resolution": {  
                "resolved_by": None,
                "reason": None,
                "timestamp": None
            },
            "created_at": datetime.utcnow()
        })

    return {
        "status": "saved",
        "patient_id": patient_id,
        "version": record["version"],
        "conflicts_found": len(conflicts),
        "conflicts": conflicts
    }


#  Existing endpoint
@router.get("/patients-with-conflicts")
def get_patients_with_conflicts():
    patients = db.conflicts.distinct("patient_id", {"status": "unresolved"})
    return {"patients": patients}


#  NEW endpoint (clinic-based)
@router.get("/patients-with-conflicts/{clinic_id}")
def get_patients_with_conflicts_by_clinic(clinic_id: str):
    patients = db.conflicts.distinct(
        "patient_id",
        {"status": "unresolved", "clinic_id": clinic_id}
    )
    return {"patients": patients}


#  Get conflicts for a patient
@router.get("/conflicts/{patient_id}")
def get_conflicts(patient_id: str):
    conflicts = list(db.conflicts.find({"patient_id": patient_id}, {"_id": 0}))
    return {"conflicts": conflicts}