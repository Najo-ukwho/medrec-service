import json
from pathlib import Path

# ✅ Load rules once
rules_path = Path(__file__).resolve().parent.parent.parent / "data" / "conflict_rules.json"

with open(rules_path) as f:
    RULES = json.load(f)

DRUG_CLASSES = RULES["drug_classes"]
CONFLICTING_CLASSES = RULES["conflicting_classes"]


def detect_conflicts(snapshots):
    conflicts = []

    all_meds = {}

    # 🔹 Collect medications across sources
    for snap in snapshots:
        source = snap["source"]
        for med in snap["medications"]:
            name = med["name"]
            dose = med["dose"]

            if name not in all_meds:
                all_meds[name] = []

            all_meds[name].append({
                "source": source,
                "dose": dose
            })

    # 🔥 1. Dose mismatch conflict (existing logic)
    for drug, entries in all_meds.items():
        doses = set(e["dose"] for e in entries)

        if len(doses) > 1:
            conflicts.append({
                "drug": drug,
                "type": "dose_mismatch",
                "details": entries
            })

    # 🔥 2. Drug class conflict (NEW)
    drugs = list(all_meds.keys())

    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):

            d1 = drugs[i]
            d2 = drugs[j]

            class1 = DRUG_CLASSES.get(d1)
            class2 = DRUG_CLASSES.get(d2)

            if not class1 or not class2:
                continue

            # check if class pair is conflicting
            if [class1, class2] in CONFLICTING_CLASSES or [class2, class1] in CONFLICTING_CLASSES:
                conflicts.append({
                    "drug": f"{d1} + {d2}",
                    "type": "class_conflict",
                    "details": {
                        "drug1_class": class1,
                        "drug2_class": class2
                    }
                })

    return conflicts