import pytest
from pymongo import MongoClient

client = MongoClient("mongodb+srv://naveenamj2005_db_user:nIbYpiN0bGBmZseu@cluster0.brorwls.mongodb.net/?appName=Cluster0")
db = client["medrec_db"]


def test_patients_with_unresolved_conflicts():

    # Insert test conflicts
    db.conflicts.insert_many([
        {
            "patient_id": "test_p1",
            "clinic_id": "clinic_X",
            "status": "unresolved"
        },
        {
            "patient_id": "test_p2",
            "clinic_id": "clinic_X",
            "status": "unresolved"
        },
        {
            "patient_id": "test_p3",
            "clinic_id": "clinic_X",
            "status": "resolved"
        }
    ])

    # Aggregation logic (same as your endpoint)
    patients = db.conflicts.distinct(
        "patient_id",
        {"status": "unresolved", "clinic_id": "clinic_X"}
    )

    # Assertions
    assert "test_p1" in patients
    assert "test_p2" in patients
    assert "test_p3" not in patients

    # Cleanup
    db.conflicts.delete_many({"patient_id": {"$in": ["test_p1", "test_p2", "test_p3"]}})