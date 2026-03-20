def detect_conflicts(snapshots):
    conflicts = []

    for i in range(len(snapshots)):
        for j in range(i + 1, len(snapshots)):

            meds1 = snapshots[i]["medications"]
            meds2 = snapshots[j]["medications"]

            for m1 in meds1:
                for m2 in meds2:

                    # Same drug
                    if m1["name"] == m2["name"]:

                        # Dose mismatch
                        if m1["dose"] != m2["dose"]:
                            conflicts.append({
                                "type": "dose_mismatch",
                                "drug": m1["name"],
                                "details": [m1["dose"], m2["dose"]]
                            })

                        # Status mismatch
                        if m1["status"] != m2["status"]:
                            conflicts.append({
                                "type": "status_conflict",
                                "drug": m1["name"],
                                "details": [m1["status"], m2["status"]]
                            })

    return conflicts