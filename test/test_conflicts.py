from app.services.conflict_detection import detect_conflicts


def test_no_conflict_same_dose():
    snapshots = [
        {
            "source": "clinic_emr",
            "medications": [{"name": "aspirin", "dose": "100 mg"}]
        },
        {
            "source": "hospital",
            "medications": [{"name": "aspirin", "dose": "100 mg"}]
        }
    ]

    conflicts = detect_conflicts(snapshots)
    assert len(conflicts) == 0


def test_dose_mismatch_conflict():
    snapshots = [
        {
            "source": "clinic_emr",
            "medications": [{"name": "aspirin", "dose": "100 mg"}]
        },
        {
            "source": "hospital",
            "medications": [{"name": "aspirin", "dose": "75 mg"}]
        }
    ]

    conflicts = detect_conflicts(snapshots)

    assert len(conflicts) == 1
    assert conflicts[0]["type"] == "dose_mismatch"


def test_class_conflict():
    snapshots = [
        {
            "source": "clinic_emr",
            "medications": [{"name": "lisinopril", "dose": "10 mg"}]
        },
        {
            "source": "hospital",
            "medications": [{"name": "losartan", "dose": "50 mg"}]
        }
    ]

    conflicts = detect_conflicts(snapshots)

    assert len(conflicts) == 1
    assert conflicts[0]["type"] == "class_conflict"